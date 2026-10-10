import hashlib
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parent.parent
source = (root / "util.m").read_text()
functions = source[source.index("NS_RETURNS_RETAINED NSString *generateHashFor"):
                   source.index("void respringAndReturnTo")]
checks = []
for pin, salt in [("1234", "salt"), ("123456", "a" * 128), ("è🔒", "test")]:
    expected = hashlib.sha512((pin + salt).encode()).hexdigest()
    checks.append(f'assert([generateHashFor(@"{pin}", @"{salt}") isEqualToString:@"{expected}"]);')
program = "@import Foundation;\n@import CommonCrypto;\n#include <assert.h>\n" + functions + """
int main(void) {
    @autoreleasepool {
        assert(generateHashFor(nil, @"salt") == nil);
        assert(generateHashFor(@"1234", nil) == nil);
        assert(![generateHashFor(@"1234", @"salt") isEqual:generateHashFor(@"9999", @"salt")]);
        NSString *salt = generateSalt();
        assert(salt.length == 128);
        assert([salt rangeOfCharacterFromSet:[[NSCharacterSet characterSetWithCharactersInString:@"0123456789abcdef"] invertedSet]].location == NSNotFound);
        assert(![salt isEqualToString:generateSalt()]);
""" + "\n".join(checks) + "\n    }\n}\n"
with tempfile.TemporaryDirectory(prefix="fakepass-hash-") as temp:
    temp = Path(temp)
    (temp / "check.m").write_text(program)
    subprocess.run(["xcrun", "--sdk", "macosx", "clang", "-fobjc-arc", "-fmodules",
                    f"-fmodules-cache-path={temp / 'modules'}", "-framework", "Foundation",
                    str(temp / "check.m"), "-o", str(temp / "check")], check=True)
    subprocess.run([str(temp / "check")], check=True)
print("PIN hashing checks passed")
