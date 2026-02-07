# From Claude during a discussion about Config file instantiations
# Example showing how to toggle the mode of a CONFIG attribute between
# DEBUG and PRODUCTION
#       https://claude.ai/chat/249ab7c6-c12d-4078-b552-ea0e59157955

class Config:
    def __init__(self, DEBUG=False):
        # FIRST: Store all parameters as attributes immediately
        self.DEBUG = DEBUG

        # THEN: Use attributes for all subsequent logic
        if self.DEBUG:  # ← Always use attribute, never parameter after this point
            self.ROCETS_OUTPUT_DIR = "C:/dev/rocets_output/"
            self.LOG_LEVEL = "DEBUG"
            self.ENABLE_PROFILING = True
        else:
            self.ROCETS_OUTPUT_DIR = "C:/production/rocets_output/"
            self.LOG_LEVEL = "INFO"
            self.ENABLE_PROFILING = False

        # Why this pattern is better:
        # 1. Consistent - always using self.attribute
        # 2. Clear intent - we're using the object's stored state
        # 3. Future-proof - if we add methods that modify self.DEBUG later,
        #    all code uses the same source of truth

# =============================================================================
#   ↓                                                                      ↓
#   ↓                     THIS STUFF RIGHT HERE                            ↓
#   ↓                                                                      ↓
# =============================================================================

    def toggle_debug_mode(self):
        """Example: Method that can change the debug state"""
        self.DEBUG = not self.DEBUG

        # Update dependent settings
        if self.DEBUG:
            self.LOG_LEVEL = "DEBUG"
        else:
            self.LOG_LEVEL = "INFO"

        print(f"Debug mode toggled to: {self.DEBUG}")

# =============================================================================
#   ↑                                                                      ↑
#   ↑                     THIS STUFF RIGHT HERE                            ↑
#   ↑                                                                      ↑
# =============================================================================
# This pattern makes the class more flexible and maintainable
config = Config(DEBUG=False)
print(f"Initial debug: {config.DEBUG}")  # False

config.toggle_debug_mode()
print(f"After toggle: {config.DEBUG}")   # True
