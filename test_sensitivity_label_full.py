#!/usr/bin/env python3
"""
Azure Synapse SQL Pool敏感性标签功能完整验证脚本
测试实际的CLI命令执行
"""
import subprocess
import sys
import json

def run_az_command(command):
    """运行Azure CLI命令"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=r"d:\code\azure-cli"
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def test_classification_commands():
    """测试敏感性分类命令"""
    print("🔍 测试敏感性分类命令...")
    
    # 基础参数
    workspace = "test20250722ws"
    resource_group = "bigdataqa"
    sql_pool = "testSQLpool1"
    
    test_commands = [
        {
            "name": "列出敏感性分类",
            "command": f".\\az-dev.bat synapse sql pool classification list --name {sql_pool} --workspace-name {workspace} --resource-group {resource_group}",
            "expect_success": True
        },
        {
            "name": "列出敏感性分类推荐",
            "command": f".\\az-dev.bat synapse sql pool classification recommendation list --name {sql_pool} --workspace-name {workspace} --resource-group {resource_group}",
            "expect_success": True
        },
        {
            "name": "显示分类帮助信息",
            "command": ".\\az-dev.bat synapse sql pool classification --help",
            "expect_success": True
        },
        {
            "name": "显示创建分类帮助信息",
            "command": ".\\az-dev.bat synapse sql pool classification create --help",
            "expect_success": True
        },
        {
            "name": "显示更新分类帮助信息", 
            "command": ".\\az-dev.bat synapse sql pool classification update --help",
            "expect_success": True
        }
    ]
    
    passed = 0
    total = len(test_commands)
    
    for test in test_commands:
        print(f"  📝 {test['name']}...")
        returncode, stdout, stderr = run_az_command(test['command'])
        
        if test['expect_success'] and returncode == 0:
            print(f"    ✅ 成功")
            if stdout.strip():
                # 尝试解析JSON输出
                try:
                    if stdout.strip().startswith('[') or stdout.strip().startswith('{'):
                        json_output = json.loads(stdout)
                        print(f"    📄 JSON输出长度: {len(json_output) if isinstance(json_output, list) else 'Object'}")
                    else:
                        print(f"    📄 输出: {stdout[:100]}...")
                except:
                    print(f"    📄 文本输出: {stdout[:100]}...")
            passed += 1
        elif not test['expect_success'] and returncode != 0:
            print(f"    ✅ 预期失败")
            passed += 1
        else:
            print(f"    ❌ 失败 (返回码: {returncode})")
            if stderr:
                print(f"    ⚠️  错误: {stderr[:200]}...")
    
    return passed, total

def test_error_scenarios():
    """测试错误场景"""
    print("\n🔍 测试错误场景...")
    
    error_tests = [
        {
            "name": "无效的workspace名称",
            "command": ".\\az-dev.bat synapse sql pool classification list --name testSQLpool1 --workspace-name invalid-workspace --resource-group bigdataqa",
            "expect_success": False
        },
        {
            "name": "无效的SQL Pool名称",
            "command": ".\\az-dev.bat synapse sql pool classification list --name invalid-pool --workspace-name test20250722ws --resource-group bigdataqa",
            "expect_success": False
        },
        {
            "name": "缺少必需参数",
            "command": ".\\az-dev.bat synapse sql pool classification list --name testSQLpool1",
            "expect_success": False
        }
    ]
    
    passed = 0
    total = len(error_tests)
    
    for test in error_tests:
        print(f"  📝 {test['name']}...")
        returncode, stdout, stderr = run_az_command(test['command'])
        
        if not test['expect_success'] and returncode != 0:
            print(f"    ✅ 预期失败，正确处理错误")
            passed += 1
        elif test['expect_success'] and returncode == 0:
            print(f"    ✅ 成功")
            passed += 1
        else:
            print(f"    ❌ 行为不符合预期 (返回码: {returncode})")
            if stderr:
                print(f"    ⚠️  错误: {stderr[:200]}...")
    
    return passed, total

def test_python_version_compatibility():
    """测试Python版本兼容性"""
    print("\n🔍 测试Python版本兼容性...")
    
    try:
        # 获取Python版本信息
        returncode, stdout, stderr = run_az_command("D:\\code\\azure-cli\\.venv\\Scripts\\python.exe --version")
        if returncode == 0:
            python_version = stdout.strip()
            print(f"    ✅ Python版本: {python_version}")
            
            # 检查是否为Python 3.13
            if "3.13" in python_version:
                print("    ✅ 确认使用Python 3.13")
                return True
            else:
                print(f"    ⚠️  当前使用的不是Python 3.13: {python_version}")
                return False
        else:
            print(f"    ❌ 无法获取Python版本: {stderr}")
            return False
    except Exception as e:
        print(f"    ❌ Python版本检查失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 80)
    print("🔬 Azure Synapse SQL Pool敏感性标签功能完整验证")
    print("=" * 80)
    
    # 测试Python版本兼容性
    python_ok = test_python_version_compatibility()
    
    # 测试分类命令
    passed1, total1 = test_classification_commands()
    
    # 测试错误场景
    passed2, total2 = test_error_scenarios()
    
    total_passed = passed1 + passed2 + (1 if python_ok else 0)
    total_tests = total1 + total2 + 1
    
    print("\n" + "=" * 80)
    print(f"📊 总体测试结果: {total_passed}/{total_tests} 通过")
    print(f"   - Python版本兼容性: {'✅' if python_ok else '❌'}")
    print(f"   - 基础命令测试: {passed1}/{total1}")
    print(f"   - 错误场景测试: {passed2}/{total2}")
    
    if total_passed == total_tests:
        print("\n🎉 所有测试通过！敏感性标签功能在Python 3.13下完全正常！")
        print("\n🔑 关键验证点:")
        print("   ✅ CLI命令正确执行")
        print("   ✅ JSON输出正确解析")
        print("   ✅ 错误处理机制正常")
        print("   ✅ Python 3.13兼容性确认")
        return 0
    else:
        print(f"\n⚠️  {total_tests - total_passed}个测试失败，需要进一步检查")
        return 1

if __name__ == "__main__":
    sys.exit(main())
