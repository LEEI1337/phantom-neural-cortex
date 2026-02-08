import os
import sys
import ast
import subprocess

def check_syntax(directory):
    print(f"Checking syntax in {directory}...")
    errors = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        ast.parse(f.read())
                except SyntaxError as e:
                    print(f"❌ Syntax Error in {path}: {e}")
                    errors += 1
                except Exception as e:
                    print(f"⚠️ Error reading {path}: {e}")
    return errors

def check_imports():
    print("Checking core components imports...")
    try:
        # We need to simulate the environment
        sys.path.insert(0, os.path.abspath("."))
        sys.path.insert(0, os.path.abspath("dashboard/backend"))
        
        print("Testing gateway imports...")
        import gateway.server
        import gateway.session
        import gateway.router
        print("✅ Gateway imports OK")
        
        print("Testing skills imports...")
        import skills.registry
        import skills.base
        import skills.loader
        print("✅ Skills imports OK")
        
        return True
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during import check: {e}")
        return False

def check_security():
    print("Performing basic security scan...")
    dangerous_functions = ["eval(", "exec(", "os.system(", "subprocess.Popen(shell=True"]
    findings = 0
    for root, _, files in os.walk("."):
        if ".git" in root or "venv" in root:
            continue
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        for func in dangerous_functions:
                            if func in content:
                                # Exclude sandbox and tests
                                if "sandbox.py" not in path and "test" not in path:
                                    print(f"⚠️ Security Warning: Dangerous function '{func}' found in {path}")
                                    findings += 1
                except:
                    pass
    return findings

if __name__ == "__main__":
    print("=== PHANTOM NEURAL CORTEX v3.0 TEST SUITE ===")
    
    syntax_errors = check_syntax(".")
    import_ok = check_imports()
    security_findings = check_security()
    
    print("\n=== RESULTS ===")
    print(f"Syntax Errors: {syntax_errors}")
    print(f"Imports: {'✅ OK' if import_ok else '❌ FAILED'}")
    print(f"Security Findings: {security_findings}")
    
    if syntax_errors == 0 and import_ok:
        print("\n🚀 PROJECT IS STABLE 🚀")
    else:
        print("\n⚠️ PROJECT HAS ISSUES ⚠️")
        sys.exit(1)
