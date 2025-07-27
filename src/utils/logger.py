"""Logging utility for the QA automation framework."""

import logging
import sys
from typing import Optional
import colorlog


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a configured logger instance.
    
    Args:
        name: Logger name. If None, uses the calling module name.
        
    Returns:
        Configured logger instance.
    """
    logger_name = name or __name__
    logger = logging.getLogger(logger_name)
    
    if not logger.handlers:
        # Create console handler with color formatting
        handler = colorlog.StreamHandler(sys.stdout)
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s%(reset)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        
    return logger 