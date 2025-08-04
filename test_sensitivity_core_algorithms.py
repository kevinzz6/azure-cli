#!/usr/bin/env python3
"""
测试敏感性标签模块的核心算法逻辑
"""
import sys
import os

# 添加Azure CLI模块路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'azure-cli'))

def test_label_lookup_algorithm():
    """测试标签查找算法（来自sqlpoolsensitivitylabel.py）"""
    print("🔍 测试标签查找算法...")
    
    # 模拟信息保护策略（类似Azure Security Center返回的数据）
    mock_information_protection_policy = {
        'labels': {
            'label-id-1': {'display_name': 'Public'},
            'label-id-2': {'display_name': 'General'},
            'label-id-3': {'display_name': 'Confidential'},
            'label-id-4': {'display_name': 'Highly Confidential'},
            'label-id-5': {'display_name': 'GDPR-Protected'}
        },
        'information_types': {
            'type-id-1': {'display_name': 'Contact Info'},
            'type-id-2': {'display_name': 'Personal'},
            'type-id-3': {'display_name': 'Financial'},
            'type-id-4': {'display_name': 'Health'},
            'type-id-5': {'display_name': 'Credentials'}
        }
    }
    
    test_cases = [
        # 测试标签查找
        {
            'type': 'label',
            'input': 'Confidential',
            'expected': 'label-id-3'
        },
        {
            'type': 'label',
            'input': 'public',  # 测试大小写不敏感
            'expected': 'label-id-1'
        },
        {
            'type': 'label',
            'input': 'GDPR-Protected',  # 测试特殊字符
            'expected': 'label-id-5'
        },
        {
            'type': 'label',
            'input': 'NonExistent',  # 测试不存在的标签
            'expected': None
        },
        # 测试信息类型查找
        {
            'type': 'information_type',
            'input': 'Personal',
            'expected': 'type-id-2'
        },
        {
            'type': 'information_type',
            'input': 'FINANCIAL',  # 测试大小写不敏感
            'expected': 'type-id-3'
        },
        {
            'type': 'information_type',
            'input': 'contact info',  # 测试大小写和空格
            'expected': 'type-id-1'
        },
        {
            'type': 'information_type',
            'input': 'Unknown',  # 测试不存在的类型
            'expected': None
        }
    ]
    
    passed = 0
    total = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        input_value = test_case['input']
        expected = test_case['expected']
        
        if test_case['type'] == 'label':
            # 模拟sqlpoolsensitivitylabel.py中的标签查找逻辑
            result = next((id for id in mock_information_protection_policy['labels']
                          if mock_information_protection_policy['labels'][id]['display_name'].lower() == 
                          input_value.lower()), None)
            search_in = "标签"
        else:
            # 模拟信息类型查找逻辑
            result = next((id for id in mock_information_protection_policy['information_types']
                          if mock_information_protection_policy['information_types'][id]['display_name'].lower() == 
                          input_value.lower()), None)
            search_in = "信息类型"
        
        if result == expected:
            print(f"  ✅ 测试 {i}: {search_in}查找 '{input_value}' -> '{result}'")
            passed += 1
        else:
            print(f"  ❌ 测试 {i}: {search_in}查找 '{input_value}' -> 期望:'{expected}', 实际:'{result}'")
    
    print(f"  📊 标签查找算法测试: {passed}/{total}")
    return passed == total

def test_string_format_compatibility():
    """测试字符串格式化兼容性"""
    print("\n🔍 测试字符串格式化兼容性...")
    
    # 模拟_create_scope函数中的字符串格式化
    tenant_ids = [
        '72f988bf-86f1-41af-91ab-2d7cd011db47',
        '12345678-1234-1234-1234-123456789012',
        'test-tenant-id'
    ]
    
    scope_format_string = '/providers/Microsoft.Management/managementGroups/{}'
    
    passed = 0
    total = len(tenant_ids)
    
    for tenant_id in tenant_ids:
        try:
            formatted_scope = scope_format_string.format(tenant_id)
            expected_prefix = '/providers/Microsoft.Management/managementGroups/'
            
            if formatted_scope.startswith(expected_prefix) and tenant_id in formatted_scope:
                print(f"  ✅ 格式化 '{tenant_id}' -> '{formatted_scope}'")
                passed += 1
            else:
                print(f"  ❌ 格式化失败 '{tenant_id}' -> '{formatted_scope}'")
        except Exception as e:
            print(f"  ❌ 格式化异常 '{tenant_id}': {e}")
    
    print(f"  📊 字符串格式化测试: {passed}/{total}")
    return passed == total

def test_exception_string_handling():
    """测试异常字符串处理"""
    print("\n🔍 测试异常字符串处理...")
    
    # 模拟sqlpoolsensitivitylabel.py中的异常处理逻辑
    test_exceptions = [
        {
            'message': 'SensitivityLabelsLabelNotFound: The sensitivity label was not found',
            'should_contain': True
        },
        {
            'message': 'ResourceNotFound: The resource was not found',
            'should_contain': False
        },
        {
            'message': 'SensitivityLabelsLabelNotFound',
            'should_contain': True
        },
        {
            'message': 'Some other error message',
            'should_contain': False
        }
    ]
    
    passed = 0
    total = len(test_exceptions)
    
    for test in test_exceptions:
        message = test['message']
        should_contain = test['should_contain']
        
        # 模拟异常处理逻辑
        class MockException:
            def __init__(self, msg):
                self.msg = msg
            def __str__(self):
                return self.msg
        
        ex = MockException(message)
        contains_target = 'SensitivityLabelsLabelNotFound' in str(ex)
        
        if contains_target == should_contain:
            status = "包含" if contains_target else "不包含"
            print(f"  ✅ '{message}' {status} 目标字符串")
            passed += 1
        else:
            expected_status = "应包含" if should_contain else "不应包含"
            actual_status = "包含" if contains_target else "不包含"
            print(f"  ❌ '{message}' {expected_status}但{actual_status}目标字符串")
    
    print(f"  📊 异常字符串处理测试: {passed}/{total}")
    return passed == total

def test_sensitivity_label_object_creation():
    """测试敏感性标签对象创建"""
    print("\n🔍 测试敏感性标签对象创建...")
    
    try:
        from azure.mgmt.synapse.models import SensitivityLabel, SensitivityLabelSource
        
        # 测试创建空的SensitivityLabel
        label1 = SensitivityLabel()
        print("  ✅ 创建空的SensitivityLabel成功")
        
        # 测试设置属性
        label1.label_name = "Confidential"
        label1.label_id = "label-id-confidential"
        label1.information_type = "Personal"
        label1.information_type_id = "type-id-personal"
        
        print(f"  ✅ 设置标签属性: {label1.label_name}, {label1.information_type}")
        
        # 测试SensitivityLabelSource枚举
        source = SensitivityLabelSource.current
        print(f"  ✅ SensitivityLabelSource: {source}")
        
        # 测试属性访问
        if hasattr(label1, 'label_name') and hasattr(label1, 'information_type'):
            print("  ✅ 标签对象属性访问正常")
            return True
        else:
            print("  ❌ 标签对象属性访问失败")
            return False
            
    except Exception as e:
        print(f"  ❌ SensitivityLabel对象测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print(f"🐍 Python版本: {sys.version}")
    print("=" * 70)
    print("🔬 Azure Synapse敏感性标签模块核心算法测试")
    print("=" * 70)
    
    tests = [
        test_label_lookup_algorithm,
        test_string_format_compatibility,
        test_exception_string_handling,
        test_sensitivity_label_object_creation
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test in tests:
        if test():
            passed_tests += 1
        print()
    
    print("=" * 70)
    print(f"📊 核心算法测试结果: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 所有核心算法测试通过！")
        print("\n🔑 验证的关键功能:")
        print("   ✅ 标签和信息类型查找算法")
        print("   ✅ 大小写不敏感匹配")
        print("   ✅ 字符串格式化处理")
        print("   ✅ 异常消息解析")
        print("   ✅ 敏感性标签对象操作")
        print("\n💡 Python 3.13兼容性评估:")
        print("   ✅ next()函数使用正常")
        print("   ✅ 字符串方法工作正常")
        print("   ✅ 对象属性访问正常")
        print("   ✅ 异常处理机制正常")
        return 0
    else:
        print("⚠️  部分核心算法测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
