import pandas as pd
import os
from dedup_service import DataDedupService


def create_sample_data():
    data = {
        'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'name': ['张三', '李四', '王五', '张三', '赵六', '李四', '孙七', '周八', '王五', '吴九'],
        'email': [
            'zhangsan@example.com',
            'lisi@example.com',
            'wangwu@example.com',
            'zhangsan@example.com',
            'zhaoliu@example.com',
            'lisi@example.com',
            'sunqi@example.com',
            'zhouba@example.com',
            'wangwu@example.com',
            'wujiu@example.com'
        ],
        'age': [25, 30, 28, 25, 35, 30, 22, 40, 28, 33]
    }

    df = pd.DataFrame(data)
    sample_path = 'sample_data.csv'
    df.to_csv(sample_path, index=False, encoding='utf-8-sig')
    print(f"测试数据已创建: {sample_path}")
    print("原始数据:")
    print(df)
    print("\n")
    return sample_path


def example_1_dedup_all_columns():
    print("=" * 60)
    print("示例 1: 基于所有列去重")
    print("=" * 60)

    service = DataDedupService()
    df_dedup = service.deduplicate(
        source='sample_data.csv',
        subset=None,
        keep='first',
        output_path='dedup_all_columns.csv'
    )

    service.print_stats()
    print("去重后的数据:")
    print(df_dedup)
    print("\n")


def example_2_dedup_specific_columns():
    print("=" * 60)
    print("示例 2: 基于指定列去重 (name + email)")
    print("=" * 60)

    service = DataDedupService()
    df_dedup = service.deduplicate(
        source='sample_data.csv',
        subset=['name', 'email'],
        keep='first',
        output_path='dedup_name_email.csv'
    )

    service.print_stats()
    print("去重后的数据:")
    print(df_dedup)
    print("\n")


def example_3_dedup_single_column():
    print("=" * 60)
    print("示例 3: 基于单列去重 (name)")
    print("=" * 60)

    service = DataDedupService()
    df_dedup = service.deduplicate(
        source='sample_data.csv',
        subset=['name'],
        keep='last',
        output_path='dedup_name_last.csv'
    )

    service.print_stats()
    print("去重后的数据 (保留最后一条):")
    print(df_dedup)
    print("\n")


def example_4_find_duplicates():
    print("=" * 60)
    print("示例 4: 查找重复数据")
    print("=" * 60)

    service = DataDedupService()
    duplicates = service.find_duplicates(
        source='sample_data.csv',
        subset=['name', 'email'],
        keep='first'
    )

    print("重复的数据 (第一条除外):")
    print(duplicates)
    print("\n")


def example_5_get_duplicate_groups():
    print("=" * 60)
    print("示例 5: 获取重复数据分组")
    print("=" * 60)

    service = DataDedupService()
    dup_groups = service.get_duplicate_groups(
        source='sample_data.csv',
        subset=['name', 'email']
    )

    print("重复数据分组:")
    print(dup_groups)
    print("\n")


def example_6_dedup_dataframe_directly():
    print("=" * 60)
    print("示例 6: 直接对 DataFrame 去重")
    print("=" * 60)

    df = pd.DataFrame({
        'product': ['A', 'B', 'A', 'C', 'B', 'D'],
        'price': [100, 200, 100, 300, 250, 400],
        'category': ['电子', '服装', '电子', '家居', '服装', '食品']
    })

    print("原始 DataFrame:")
    print(df)
    print()

    service = DataDedupService()
    df_dedup = service.deduplicate(
        source=df,
        subset=['product', 'price']
    )

    service.print_stats()
    print("去重后的 DataFrame:")
    print(df_dedup)
    print("\n")


def example_7_get_stats():
    print("=" * 60)
    print("示例 7: 获取去重统计信息 (编程方式)")
    print("=" * 60)

    service = DataDedupService()
    service.deduplicate('sample_data.csv', subset=['name'])

    stats = service.get_stats()
    print("统计信息字典:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print("\n")


def cleanup_files():
    files_to_remove = [
        'sample_data.csv',
        'dedup_all_columns.csv',
        'dedup_name_email.csv',
        'dedup_name_last.csv'
    ]
    for f in files_to_remove:
        if os.path.exists(f):
            os.remove(f)
            print(f"已清理文件: {f}")


if __name__ == '__main__':
    try:
        sample_file = create_sample_data()
        example_1_dedup_all_columns()
        example_2_dedup_specific_columns()
        example_3_dedup_single_column()
        example_4_find_duplicates()
        example_5_get_duplicate_groups()
        example_6_dedup_dataframe_directly()
        example_7_get_stats()
    finally:
        cleanup = input("\n是否清理生成的测试文件? (y/n): ").strip().lower()
        if cleanup == 'y':
            cleanup_files()
        print("\n所有示例运行完成!")
