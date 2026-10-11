"""Exercise the actual passcode hook with in-memory preferences and fake PINs."""
import os
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parent.parent
tweak = (root / "Tweak.xm").read_text()
start = tweak.index("- (BOOL)changePasscodeFrom:")
hook = tweak[start:tweak.index("- (BOOL)unlockDeviceWithPasscode:", start)]
checks = tweak[tweak.index("BOOL isPasscodeSet()"):
               tweak.index("BOOL doUnlock(")]
util = (root / "util.m").read_text()
hashing = util[util.index("NS_RETURNS_RETAINED NSString *generateHashFor"):
               util.index("void respringAndReturnTo")]
program = """
@import Foundation;
@import CommonCrypto;
#include <assert.h>

static NSMutableDictionary *stored;
static NSInteger resprings;
@interface TestDefaults : NSObject
- (instancetype)initWithSuiteName:(NSString *)name;
- (id)objectForKey:(NSString *)key;
- (void)setObject:(id)value forKey:(NSString *)key;
- (void)setInteger:(NSInteger)value forKey:(NSString *)key;
- (void)removeObjectForKey:(NSString *)key;
@end
@implementation TestDefaults
- (instancetype)initWithSuiteName:(NSString *)name { return [super init]; }
- (id)objectForKey:(NSString *)key { return stored[key]; }
- (void)setObject:(id)value forKey:(NSString *)key { stored[key] = value; }
- (void)setInteger:(NSInteger)value forKey:(NSString *)key { stored[key] = @(value); }
- (void)removeObjectForKey:(NSString *)key { [stored removeObjectForKey:key]; }
@end
TestDefaults *prefs;
BOOL creatingPasscode;
BOOL isInternalUnlock = NO;
void respring(void) { resprings++; }
""" + hashing + checks.replace("NSUserDefaults", "TestDefaults") + """
@interface TestConnection : NSObject
- (BOOL)changePasscodeFrom:(NSString *)oldPasscode to:(NSString *)newPasscode outError:(id *)outError;
@end
@implementation TestConnection
""" + hook.replace("NSUserDefaults", "TestDefaults") + """
@end
int main(void) {
    @autoreleasepool {
        stored = [NSMutableDictionary new];
        TestConnection *connection = [TestConnection new];
        assert([connection changePasscodeFrom:nil to:@"123456" outError:NULL]);
        assert(checkPasscode(@"123456"));
        assert(resprings == 1);
        NSDictionary *before = [stored copy];
        assert(![connection changePasscodeFrom:nil to:nil outError:NULL]);
        assert(![connection changePasscodeFrom:@"" to:@"" outError:NULL]);
        assert(![connection changePasscodeFrom:@"999999" to:nil outError:NULL]);
        assert(![connection changePasscodeFrom:nil to:@"654321" outError:NULL]);
        assert(![connection changePasscodeFrom:@"999999" to:@"654321" outError:NULL]);
        assert([stored isEqualToDictionary:before]);
        assert(resprings == 1);
        assert([connection changePasscodeFrom:@"123456" to:@"654321" outError:NULL]);
        assert(!checkPasscode(@"123456"));
        assert(checkPasscode(@"654321"));
        assert([connection changePasscodeFrom:@"654321" to:nil outError:NULL]);
        assert(!isPasscodeSet());
        assert([connection changePasscodeFrom:nil to:@"4321" outError:NULL]);
        assert(checkPasscode(@"4321"));
    }
}
"""
with tempfile.TemporaryDirectory(prefix="fakepass-changes-") as temporary:
    temporary = Path(temporary)
    source = temporary / "check.m"
    source.write_text(program)
    env = dict(os.environ)
    env.setdefault("DEVELOPER_DIR", "/Applications/Xcode.app/Contents/Developer")
    subprocess.run(["xcrun", "--sdk", "macosx", "clang", "-fobjc-arc", "-fmodules",
                    f"-fmodules-cache-path={temporary / 'modules'}", "-framework", "Foundation",
                    str(source), "-o", str(temporary / "check")], check=True, env=env)
    subprocess.run([str(temporary / "check")], check=True)
print("Passcode change authorization checks passed")
