#!/usr/bin/env python3
"""
Azure Synapse SQL Pool Python 3.13兼容性测试脚本
"""
import sys
import os

# 添加Azure CLI模块路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'azure-cli'))

def test_sqlpool_imports():
    """测试SQL Pool模块导入"""
    print("🔍 测试SQL Pool模块导入...")
    try:
        from azure.cli.command_modules.synapse.manual.operations.sqlpool import (
            create_sql_pool, 
            update_sql_pool, 
            restore_sql_pool,
            sql_pool_show_connection_string,
            _construct_database_resource_id
        )
        print("✅ SQL Pool操作函数导入成功")
        
        from azure.cli.command_modules.synapse.manual.constant import (
            SynapseSqlCreateMode,
            SqlPoolConnectionClientAuthenticationType,
            SqlPoolConnectionClientType
        )
        print("✅ SQL Pool常量导入成功")
        
        return True
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_connection_string_function():
    """测试连接字符串生成函数"""
    print("\n🔍 测试连接字符串生成函数...")
    try:
        from azure.cli.command_modules.synapse.manual.operations.sqlpool import sql_pool_show_connection_string
        from azure.cli.command_modules.synapse.manual.constant import (
            SqlPoolConnectionClientAuthenticationType,
            SqlPoolConnectionClientType
        )
        
        # 模拟CLI上下文
        class MockSuffixes:
            synapse_analytics_endpoint = '.dev.azuresynapse.net'
        
        class MockCloud:
            suffixes = MockSuffixes()
        
        class MockCliCtx:
            cloud = MockCloud()
        
        class MockCmd:
            cli_ctx = MockCliCtx()
        
        mock_cmd = MockCmd()
        
        # 测试ADO.NET连接字符串
        result = sql_pool_show_connection_string(
            mock_cmd,
            SqlPoolConnectionClientType.AdoDotNet,
            'testsqlpool',
            'testworkspace',
            SqlPoolConnectionClientAuthenticationType.SqlPassword.value
        )
        print(f"✅ ADO.NET连接字符串: {result[:50]}...")
        
        # 测试JDBC连接字符串
        result = sql_pool_show_connection_string(
            mock_cmd,
            SqlPoolConnectionClientType.Jdbc,
            'testsqlpool', 
            'testworkspace',
            SqlPoolConnectionClientAuthenticationType.SqlPassword.value
        )
        print(f"✅ JDBC连接字符串: {result[:50]}...")
        
        # 测试PHP PDO连接字符串
        result = sql_pool_show_connection_string(
            mock_cmd,
            SqlPoolConnectionClientType.PhpPdo,
            'testsqlpool',
            'testworkspace', 
            SqlPoolConnectionClientAuthenticationType.SqlPassword.value
        )
        print(f"✅ PHP PDO连接字符串: {result[:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ 连接字符串生成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_url_quote_function():
    """测试URL编码函数（Python 3.13中可能有变化）"""
    print("\n🔍 测试URL编码函数...")
    try:
        from urllib.parse import quote
        
        # 测试各种特殊字符
        test_cases = [
            "normal-name",
            "name with spaces",
            "name@with#special$chars",
            "中文名称",
            "name/with/slashes"
        ]
        
        for test_case in test_cases:
            encoded = quote(test_case)
            print(f"✅ '{test_case}' -> '{encoded}'")
        
        return True
    except Exception as e:
        print(f"❌ URL编码测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_enum_usage():
    """测试枚举类型使用（Python 3.13可能有优化）"""
    print("\n🔍 测试枚举类型使用...")
    try:
        from azure.cli.command_modules.synapse.manual.constant import (
            SynapseSqlCreateMode,
            SqlPoolConnectionClientAuthenticationType,
            SqlPoolConnectionClientType
        )
        
        # 测试枚举值访问
        print(f"✅ SynapseSqlCreateMode.Default: {SynapseSqlCreateMode.Default}")
        print(f"✅ SqlPoolConnectionClientType.AdoDotNet: {SqlPoolConnectionClientType.AdoDotNet}")
        print(f"✅ SqlPoolConnectionClientAuthenticationType.SqlPassword: {SqlPoolConnectionClientAuthenticationType.SqlPassword}")
        
        # 测试枚举比较
        assert SynapseSqlCreateMode.Default == SynapseSqlCreateMode.Default
        assert SqlPoolConnectionClientType.AdoDotNet != SqlPoolConnectionClientType.Jdbc
        print("✅ 枚举比较正常")
        
        # 测试枚举值属性
        auth_type = SqlPoolConnectionClientAuthenticationType.SqlPassword.value
        print(f"✅ 枚举值属性: {auth_type}")
        
        return True
    except Exception as e:
        print(f"❌ 枚举测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_exception_handling():
    """测试异常处理（在Python 3.13中可能有改进）"""
    print("\n🔍 测试异常处理...")
    try:
        from azure.cli.command_modules.synapse.manual.operations.sqlpool import sql_pool_show_connection_string
        from azure.cli.command_modules.synapse.manual.constant import (
            SqlPoolConnectionClientAuthenticationType,
            SqlPoolConnectionClientType
        )
        from knack.util import CLIError
        
        # 模拟CLI上下文
        class MockSuffixes:
            synapse_analytics_endpoint = '.dev.azuresynapse.net'
        
        class MockCloud:
            suffixes = MockSuffixes()
        
        class MockCliCtx:
            cloud = MockCloud()
        
        class MockCmd:
            cli_ctx = MockCliCtx()
        
        mock_cmd = MockCmd()
        
        # 测试PHP驱动程序限制的异常处理
        try:
            sql_pool_show_connection_string(
                mock_cmd,
                SqlPoolConnectionClientType.Php,
                'testsqlpool',
                'testworkspace',
                SqlPoolConnectionClientAuthenticationType.ActiveDirectoryPassword.value
            )
            print("❌ 应该抛出异常但没有")
            return False
        except CLIError as e:
            print(f"✅ 正确抛出CLIError: {e}")
        
        # 测试PHP PDO驱动程序限制的异常处理
        try:
            sql_pool_show_connection_string(
                mock_cmd,
                SqlPoolConnectionClientType.PhpPdo,
                'testsqlpool',
                'testworkspace',
                SqlPoolConnectionClientAuthenticationType.ActiveDirectoryIntegrated.value
            )
            print("❌ 应该抛出异常但没有")
            return False
        except CLIError as e:
            print(f"✅ 正确抛出CLIError: {e}")
        
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
    print("=" * 60)
    
    tests = [
        test_sqlpool_imports,
        test_connection_string_function,
        test_url_quote_function,
        test_enum_usage,
        test_exception_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！Azure Synapse SQL Pool在Python 3.13下运行正常！")
        return 0
    else:
        print("⚠️  部分测试失败，需要进一步检查兼容性问题")
        return 1

if __name__ == "__main__":
    sys.exit(main())
