export THEOS_PACKAGE_SCHEME = rootless
TARGET := iphone:clang:16.5:16.5

INSTALL_TARGET_PROCESSES = SpringBoard Preferences

ARCHS = arm64e

include $(THEOS)/makefiles/common.mk

TWEAK_NAME = FakePass

FakePass_FILES = Tweak.xm util.m
FakePass_CFLAGS = -fobjc-arc -Wno-error
FakePass_LIBRARIES = sandy
FakePass_PRIVATE_FRAMEWORKS = FrontBoardServices SpringBoardServices

include $(THEOS_MAKE_PATH)/tweak.mk
SUBPROJECTS += prefs
include $(THEOS_MAKE_PATH)/aggregate.mk
