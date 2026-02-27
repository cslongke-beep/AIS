"""
Excel 数据清洗脚本
功能：检测并处理缺失值、重复值
"""

import sys
import pandas as pd


def load_excel(file_path: str, sheet_name=0) -> pd.DataFrame:
    """加载 Excel 文件"""
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"[OK] 成功读取文件: {file_path}")
        print(f"     共 {df.shape[0]} 行 x {df.shape[1]} 列\n")
        return df
    except FileNotFoundError:
        print(f"[ERROR] 文件不存在: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] 读取失败: {e}")
        sys.exit(1)


def overview(df: pd.DataFrame):
    """数据概览"""
    print("=" * 50)
    print("【数据概览】")
    print("=" * 50)
    print(df.dtypes.to_string())
    print()


def analyze_missing(df: pd.DataFrame) -> pd.DataFrame:
    """缺失值分析"""
    print("=" * 50)
    print("【缺失值分析】")
    print("=" * 50)

    total = df.shape[0]
    missing = df.isnull().sum()
    missing_pct = (missing / total * 100).round(2)

    report = pd.DataFrame({
        "缺失数量": missing,
        "缺失比例(%)": missing_pct
    })
    report = report[report["缺失数量"] > 0].sort_values("缺失数量", ascending=False)

    if report.empty:
        print("无缺失值\n")
    else:
        print(report.to_string())
        print()

    return report


def analyze_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """重复值分析"""
    print("=" * 50)
    print("【重复值分析】")
    print("=" * 50)

    dup_rows = df[df.duplicated(keep=False)]
    dup_count = df.duplicated().sum()

    print(f"重复行数量: {dup_count}")

    if dup_count > 0:
        print(f"重复行示例（前 5 行）:")
        print(dup_rows.head(5).to_string())
    print()

    return dup_rows


def clean_data(df: pd.DataFrame, drop_duplicates=True, fill_missing=None) -> pd.DataFrame:
    """
    数据清洗
    :param drop_duplicates: 是否删除重复行
    :param fill_missing: 缺失值填充策略，可选 'mean' / 'median' / 'mode' / None（直接删除）
    """
    print("=" * 50)
    print("【数据清洗】")
    print("=" * 50)

    original_rows = df.shape[0]
    df = df.copy()

    # 处理重复值
    if drop_duplicates:
        df = df.drop_duplicates()
        removed = original_rows - df.shape[0]
        print(f"已删除重复行: {removed} 行")

    # 处理缺失值
    if fill_missing == "mean":
        num_cols = df.select_dtypes(include="number").columns
        df[num_cols] = df[num_cols].fillna(df[num_cols].mean())
        print("数值列缺失值已用【均值】填充")
    elif fill_missing == "median":
        num_cols = df.select_dtypes(include="number").columns
        df[num_cols] = df[num_cols].fillna(df[num_cols].median())
        print("数值列缺失值已用【中位数】填充")
    elif fill_missing == "mode":
        for col in df.columns:
            df[col] = df[col].fillna(df[col].mode().iloc[0] if not df[col].mode().empty else df[col])
        print("所有列缺失值已用【众数】填充")
    else:
        before = df.shape[0]
        df = df.dropna()
        removed = before - df.shape[0]
        print(f"已删除含缺失值的行: {removed} 行")

    print(f"清洗后: {df.shape[0]} 行 x {df.shape[1]} 列\n")
    return df


def save_excel(df: pd.DataFrame, output_path: str):
    """保存清洗后的数据"""
    df.to_excel(output_path, index=False)
    print(f"[OK] 已保存清洗结果到: {output_path}")


def main():
    # -----------------------------------------------
    # 配置区域 - 根据实际情况修改以下参数
    # -----------------------------------------------
    INPUT_FILE = "data.xlsx"          # 输入文件路径
    OUTPUT_FILE = "data_cleaned.xlsx" # 输出文件路径
    SHEET_NAME = 0                    # Sheet 名称或索引（0 表示第一个）

    # 缺失值处理策略: 'mean' | 'median' | 'mode' | None（None 表示删除含缺失值的行）
    FILL_MISSING = None

    DROP_DUPLICATES = True            # 是否删除重复行
    # -----------------------------------------------

    df = load_excel(INPUT_FILE, sheet_name=SHEET_NAME)
    overview(df)
    analyze_missing(df)
    analyze_duplicates(df)

    df_clean = clean_data(df, drop_duplicates=DROP_DUPLICATES, fill_missing=FILL_MISSING)

    save_excel(df_clean, OUTPUT_FILE)


if __name__ == "__main__":
    main()
