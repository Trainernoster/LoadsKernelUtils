import logging
import time
from datetime import datetime

BAR_WIDTH = 40              # Char length of the progress bar
STEP_SIZE = 5               # Percentage step of the progress bar (accuracy)
N_STEPS = 100 // STEP_SIZE  # Number of interval steps until progress ends   

def _fmt(seconds: float) -> str:
    # Convert time float into string
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return f'{h:02}:{m:02}:{s:02}'

def _bar(step: int) -> str:
    # Calculate bar progress in string pattern
    if step > N_STEPS:
        return '|' + '*' * BAR_WIDTH + '|'
    filled = step * BAR_WIDTH // N_STEPS
    return '|' + '=' * filled + ' ' * (BAR_WIDTH - filled) + '|'

class ProgressLogger:
    def __init__(self) -> None:
        self.reset()

    @staticmethod
    def _log_header(tmax: float) -> None:
        logging.info(
            f'  Time   | Duration | {STEP_SIZE:2}% Duration | Progress   0%: {_bar(0)} '
            f'Sim time: 0.000sec of {tmax}sec.'
        )

    @staticmethod
    def _log_row(now: float, begin: float, last: float, current: int | None = None, tail: str | None = None) -> None:
        _clock = datetime.now().strftime('%H:%M:%S')
        _total = _fmt(now - begin)
        _interval = _fmt(now - last)
        if current is None:
            _progress = '100'
            current = N_STEPS
        else:
            _progress = 'err' if current > N_STEPS else f'{current * STEP_SIZE:>3}'
        _tail = '' if tail is None else tail
        logging.info(f'{_clock} | {_total} |   {_interval}   | Progress {_progress}%: {_bar(current)} {_tail}')

    def reset(self) -> None:
        # Reset the logger after the progress finished
        self._begin: float | None = None
        self._tmax: float = 0.0
        self._last_time: float = 0.0
        self._last_logged_step: int = 0

    def begin(self, tmax: float) -> None:
        if self._begin is None:
            if tmax <= 0:
                # tmax must be greater than zero
                return
            # Print initial duration
            self._begin = self._last_time = time.perf_counter()
            self._tmax = tmax

            # Logging progress header
            self._log_header(tmax= tmax)

    def update(self, t: float) -> None:
        if self._begin is None:
            return
        # Calculate current progress step
        current_step = int(t * N_STEPS / self._tmax)
        if current_step <= self._last_logged_step or current_step >= N_STEPS:
            # Exit if current step do not exceed next logging stage
            # Exit if counter would display full stage if it is not 100%
            return

        # Prepare current step for logging
        now = time.perf_counter()
        label = f'Sim time: {t:.3f}sec of {self._tmax}sec.'

        # Log current step
        self._log_row(now=now, begin=self._begin, last=self._last_time, tail=label, current=current_step)

        # Update stored steps
        self._last_time = now
        self._last_logged_step = current_step

    def end(self) -> None:
        if self._begin is None:
            return
        now = time.perf_counter()
        total = _fmt(now - self._begin)
        label = f'Done in {total}.'

        # Log last row
        self._log_row(now=now, begin=self._begin, last=self._last_time, tail=label)
        self.reset()