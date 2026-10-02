// Copyright (c) 2026 Stompi
// Distributed under the MIT software license, see the accompanying LICENSE.
// Pool-local work accounting: old jobs retain their original share targets.
use std::time::Instant;

// A difficulty-one Bitcoin/Stompi target requires ~2^32 * 65536/65535 hashes.
const HASHES_PER_DIFFICULTY: f64 = 4294967296.0 * 65536.0 / 65535.0;

#[derive(Debug)]
pub(crate) struct VardiffState {
    window_start: Instant,
    accepted_work: f64,
}

impl VardiffState {
    pub(crate) fn new() -> Self {
        Self { window_start: Instant::now(), accepted_work: 0.0 }
    }

    pub(crate) fn record_accepted_work(&mut self, work: f64) {
        if work.is_finite() && work > 0.0 {
            let total = self.accepted_work + work;
            if total.is_finite() { self.accepted_work = total; }
        }
    }

    pub(crate) fn try_vardiff(&mut self, hashrate: f32, shares_per_minute: f32)
        -> Option<f32>
    {
        self.update_after(hashrate, shares_per_minute, self.window_start.elapsed().as_secs_f64())
    }

    fn update_after(&mut self, hashrate: f32, shares_per_minute: f32, seconds: f64) -> Option<f32> {
        if !seconds.is_finite() || seconds <= 15.0
            || !shares_per_minute.is_finite() || shares_per_minute <= 0.0 {
            return None;
        }
        let baseline = if hashrate.is_finite() { (hashrate as f64).max(1.0) } else { 1.0 };
        let estimate = self.accepted_work * HASHES_PER_DIFFICULTY / seconds;
        if !estimate.is_finite() { return None; }
        let pct = (estimate - baseline).abs() / baseline * 100.0;
        // Preserve upstream update thresholds and extreme-change limits.
        let change = pct >= 100.0 || (pct >= 60.0 && seconds >= 60.0)
            || (pct >= 50.0 && seconds >= 120.0) || (pct >= 45.0 && seconds >= 180.0)
            || (pct >= 30.0 && seconds >= 240.0) || (pct >= 15.0 && seconds >= 300.0);
        if !change { return None; }
        let adjusted = if self.accepted_work == 0.0 {
            baseline / if seconds <= 30.0 { 1.5 } else if seconds < 60.0 { 2.0 } else { 3.0 }
        } else if pct > 1000.0 {
            baseline * if seconds <= 30.0 { 10.0 } else if seconds < 60.0 { 5.0 } else { 3.0 }
        } else { estimate };
        let result = adjusted.clamp(1.0, f32::MAX as f64) as f32;
        self.accepted_work = 0.0;
        self.window_start = Instant::now();
        Some(result)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn old_jobs_do_not_gain_work_when_channel_target_changes() {
        let mut state = VardiffState::new();
        // Ten accepted old-job shares, each difficulty 2328, during 60 seconds.
        for _ in 0..10 { state.record_accepted_work(2328.0); }
        let expected = 23280.0 * HASHES_PER_DIFFICULTY / 60.0;
        let result = state.update_after(100e12, 6.0, 60.0).unwrap() as f64;
        assert!((result / expected - 1.0).abs() < 1e-6);
        assert!(result < 2e12);
    }
    #[test]
    fn mixed_job_targets_are_weighted_by_accepted_work() {
        let mut state = VardiffState::new();
        state.record_accepted_work(1000.0);
        state.record_accepted_work(5000.0);
        let expected = 6000.0 * HASHES_PER_DIFFICULTY / 60.0;
        let result = state.update_after(2e12, 6.0, 60.0).unwrap() as f64;
        assert!((result / expected - 1.0).abs() < 1e-6);
    }
    #[test]
    fn invalid_work_cannot_inflate_estimate() {
        let mut state = VardiffState::new();
        for work in [0.0, -1.0, f64::NAN, f64::INFINITY] { state.record_accepted_work(work); }
        assert_eq!(state.accepted_work, 0.0);
        assert_eq!(state.update_after(1e12, 6.0, 60.0), Some(1e12_f32 / 3.0));
    }
    #[test]
    fn update_resets_work_but_short_window_keeps_it() {
        let mut state = VardiffState::new();
        state.record_accepted_work(2328.0);
        assert_eq!(state.update_after(1e12, 6.0, 10.0), None);
        assert_eq!(state.accepted_work, 2328.0);
        assert!(state.update_after(1e12, 6.0, 60.0).is_some());
        assert_eq!(state.accepted_work, 0.0);
    }
    #[test]
    fn stable_1_8_th_does_not_run_away() {
        let mut state = VardiffState::new();
        state.record_accepted_work(1.8e12 * 300.0 / HASHES_PER_DIFFICULTY);
        assert_eq!(state.update_after(1.8e12, 6.0, 300.0), None);
    }
}
