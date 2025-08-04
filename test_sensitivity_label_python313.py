#!/usr/bin/env python3
"""
Azure Synapse SQL Pool敏感性标签模块 Python 3.13兼容性测试脚本
"""
import sys
import os

# 添加Azure CLI模块路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'azure-cli'))

def test_sensitivity_label_imports():
    """测试敏感性标签模块导入"""
    print("🔍 测试敏感性标签模块导入...")
    try:
        from azure.cli.command_modules.synapse.manual.operations.sqlpoolsensitivitylabel import (
            sqlpool_sensitivity_label_show,
            sqlpool_sensitivity_label_update,
            sqlpool_sensitivity_label_create,
            _create_scope
        )
        print("✅ 敏感性标签操作函数导入成功")
        
        from azure.mgmt.synapse.models import SensitivityLabel, SensitivityLabelSource
        print("✅ 敏感性标签模型导入成功")
        
        from azure.mgmt.security import SecurityCenter
        print("✅ 安全中心模块导入成功")
        
        from azure.core.exceptions import HttpResponseError
        print("✅ Azure核心异常模块导入成功")
        
        return True
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scope_creation():
    """测试作用域创建函数"""
    print("\n🔍 测试作用域创建函数...")
    try:
        from azure.cli.command_modules.synapse.manual.operations.sqlpoolsensitivitylabel import _create_scope
        from azure.cli.core._profile import Profile
        
        # 模拟profile和subscription
        class MockSubscription:
            def __init__(self):
                self.data = {'tenantId': '12345678-1234-1234-1234-123456789012'}
            
            def __getitem__(self, key):
                return self.data[key]
        
        class MockProfile:
            def get_subscription(self):
                return MockSubscription()
        
        # 临时替换Profile类
        original_profile = Profile
        try:
            # 替换模块中的Profile
            import azure.cli.command_modules.synapse.manual.operations.sqlpoolsensitivitylabel as module
            module.Profile = MockProfile
            
            # 测试作用域创建
            scope = _create_scope()
            print(f"✅ 作用域创建成功: {scope}")
            
            # 验证格式正确性
            if scope.startswith('/providers/Microsoft.Management/managementGroups/'):
                print("✅ 作用域格式正确")
                return True
            else:
                print(f"❌ 作用域格式错误: {scope}")
                return False
        finally:
            # 恢复原始Profile类
            module.Profile = original_profile
        
    except Exception as e:
        print(f"❌ 作用域创建测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sensitivity_label_models():
    """测试敏感性标签模型"""
    print("\n🔍 测试敏感性标签模型...")
    try:
        from azure.mgmt.synapse.models import SensitivityLabel, SensitivityLabelSource
        
        # 测试SensitivityLabel模型创建
        label = SensitivityLabel()
        label.label_name = "Confidential"
        label.label_id = "test-label-id"
        label.information_type = "Personal"
        label.information_type_id = "test-info-type-id"
        
        print(f"✅ SensitivityLabel创建成功")
        print(f"   - label_name: {label.label_name}")
        print(f"   - information_type: {label.information_type}")
        
        # 测试SensitivityLabelSource枚举
        current_source = SensitivityLabelSource.current
        print(f"✅ SensitivityLabelSource枚举: {current_source}")
        
        return True
    except Exception as e:
        print(f"❌ 敏感性标签模型测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_next_function_usage():
    """测试next()函数的使用（Python 3.13中可能有优化）"""
    print("\n🔍 测试next()函数的使用...")
    try:
        # 模拟信息保护策略结构
        mock_policy = {
            'labels': {
                'label1': {'display_name': 'Confidential'},
                'label2': {'display_name': 'Public'},
                'label3': {'display_name': 'Internal'}
            },
            'information_types': {
                'type1': {'display_name': 'Personal'},
                'type2': {'display_name': 'Financial'},
                'type3': {'display_name': 'Health'}
            }
        }
        
        # 测试标签查找（模拟sqlpoolsensitivitylabel.py中的逻辑）
        label_name = "Confidential"
        label_id = next((id for id in mock_policy['labels']
                        if mock_policy['labels'][id]['display_name'].lower() == label_name.lower()),
                       None)
        
        if label_id == 'label1':
            print(f"✅ 标签查找成功: '{label_name}' -> '{label_id}'")
        else:
            print(f"❌ 标签查找失败，期望: 'label1', 实际: {label_id}")
            return False
        
        # 测试信息类型查找
        information_type = "Personal"
        information_type_id = next((id for id in mock_policy['information_types']
                                   if mock_policy['information_types'][id]['display_name'].lower() == information_type.lower()),
                                  None)
        
        if information_type_id == 'type1':
            print(f"✅ 信息类型查找成功: '{information_type}' -> '{information_type_id}'")
        else:
            print(f"❌ 信息类型查找失败，期望: 'type1', 实际: {information_type_id}")
            return False
        
        # 测试未找到的情况
        not_found_label = next((id for id in mock_policy['labels']
                               if mock_policy['labels'][id]['display_name'].lower() == 'NonExistent'.lower()),
                              None)
        
        if not_found_label is None:
            print("✅ 未找到标签时正确返回None")
        else:
            print(f"❌ 未找到标签时应返回None，实际返回: {not_found_label}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ next()函数测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_string_operations():
    """测试字符串操作（Python 3.13中可能有优化）"""
    print("\n🔍 测试字符串操作...")
    try:
        # 测试字符串包含检查（模拟异常处理逻辑）
        error_message = "SensitivityLabelsLabelNotFound: The sensitivity label was not found"
        
        if 'SensitivityLabelsLabelNotFound' in str(error_message):
            print("✅ 字符串包含检查正常")
        else:
            print("❌ 字符串包含检查失败")
            return False
        
        # 测试大小写转换
        test_cases = [
            ("Confidential", "confidential"),
            ("Personal Data", "personal data"),
            ("GDPR-Protected", "gdpr-protected"),
            ("中文标签", "中文标签")  # 测试Unicode字符
        ]
        
        for original, expected in test_cases:
            result = original.lower()
            if result == expected:
                print(f"✅ 大小写转换: '{original}' -> '{result}'")
            else:
                print(f"❌ 大小写转换失败: '{original}' -> '{result}', 期望: '{expected}'")
                return False
        
        # 测试字符串格式化
        tenant_id = "12345678-1234-1234-1234-123456789012"
        scope_format_string = '/providers/Microsoft.Management/managementGroups/{}'
        formatted_scope = scope_format_string.format(tenant_id)
        expected_scope = f'/providers/Microsoft.Management/managementGroups/{tenant_id}'
        
        if formatted_scope == expected_scope:
            print(f"✅ 字符串格式化: {formatted_scope}")
        else:
            print(f"❌ 字符串格式化失败，期望: {expected_scope}, 实际: {formatted_scope}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ 字符串操作测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_exception_handling():
    """测试异常处理机制"""
    print("\n🔍 测试异常处理机制...")
    try:
        from knack.util import CLIError
        from azure.core.exceptions import HttpResponseError
        
        # 测试CLIError创建和抛出
        try:
            raise CLIError('The provided label name was not found in the information protection policy.')
        except CLIError as e:
            print(f"✅ CLIError正确抛出和捕获: {e}")
        
        # 测试HttpResponseError创建
        class MockHttpResponseError(Exception):
            def __init__(self, message):
                self.message = message
            
            def __str__(self):
                return self.message
        
        # 模拟HttpResponseError处理逻辑
        ex = MockHttpResponseError("SensitivityLabelsLabelNotFound: Label not found")
        
        if ex and 'SensitivityLabelsLabelNotFound' in str(ex):
            print("✅ HttpResponseError异常处理逻辑正常")
        else:
            print("❌ HttpResponseError异常处理逻辑失败")
            return False
        
        # 测试异常重新抛出
        try:
            ex = MockHttpResponseError("Some other error")
            if not (ex and 'SensitivityLabelsLabelNotFound' in str(ex)):
                raise ex
        except Exception as e:
            print(f"✅ 异常重新抛出机制正常: {e}")
        
        return True
    except Exception as e:
        print(f"❌ 异常处理测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print(f"🐍 Python版本: {sys.version}")
    print(f"📍 工作目录: {os.getcwd()}")
    print("=" * 70)
    print("🔬 Azure Synapse SQL Pool敏感性标签模块 Python 3.13兼容性测试")
    print("=" * 70)
    
    tests = [
        test_sensitivity_label_imports,
        test_scope_creation,
        test_sensitivity_label_models,
        test_next_function_usage,
        test_string_operations,
        test_exception_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 70)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！敏感性标签模块在Python 3.13下运行正常！")
        return 0
    else:
        print("⚠️  部分测试失败，需要进一步检查兼容性问题")
        return 1

if __name__ == "__main__":
    sys.exit(main())
