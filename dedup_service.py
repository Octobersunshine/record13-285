import pandas as pd
from typing import List, Optional, Union, Dict, Any
import os


class DataDedupService:
    def __init__(self):
        self.stats: Dict[str, Any] = {}

    def _read_data(self, source: Union[pd.DataFrame, str], **kwargs) -> pd.DataFrame:
        if isinstance(source, pd.DataFrame):
            return source.copy()
        elif isinstance(source, str):
            file_ext = os.path.splitext(source)[1].lower()
            if file_ext == '.csv':
                return pd.read_csv(source, **kwargs)
            elif file_ext in ['.xlsx', '.xls']:
                return pd.read_excel(source, **kwargs)
            elif file_ext == '.json':
                return pd.read_json(source, **kwargs)
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
        else:
            raise TypeError("Source must be a pandas DataFrame or a file path string")

    def _write_data(self, df: pd.DataFrame, output_path: str, **kwargs) -> None:
        file_ext = os.path.splitext(output_path)[1].lower()
        if file_ext == '.csv':
            df.to_csv(output_path, index=False, **kwargs)
        elif file_ext in ['.xlsx', '.xls']:
            df.to_excel(output_path, index=False, **kwargs)
        elif file_ext == '.json':
            df.to_json(output_path, orient='records', **kwargs)
        else:
            raise ValueError(f"Unsupported output format: {file_ext}")

    def deduplicate(
        self,
        source: Union[pd.DataFrame, str],
        subset: Optional[List[str]] = None,
        keep: str = 'first',
        ignore_index: bool = True,
        output_path: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        df = self._read_data(source, **kwargs)

        original_count = len(df)

        dedup_df = df.drop_duplicates(
            subset=subset,
            keep=keep,
            ignore_index=ignore_index
        )

        dedup_count = len(dedup_df)
        removed_count = original_count - dedup_count

        self.stats = {
            'original_count': original_count,
            'dedup_count': dedup_count,
            'removed_count': removed_count,
            'duplicate_rate': (removed_count / original_count * 100) if original_count > 0 else 0,
            'subset': subset if subset else 'all_columns',
            'keep_strategy': keep
        }

        if output_path:
            self._write_data(dedup_df, output_path, **kwargs)
            self.stats['output_path'] = output_path

        return dedup_df

    def get_stats(self) -> Dict[str, Any]:
        return self.stats

    def print_stats(self) -> None:
        if not self.stats:
            print("No deduplication has been performed yet.")
            return

        print("=" * 50)
        print("数据去重统计报告")
        print("=" * 50)
        print(f"原始数据量: {self.stats['original_count']}")
        print(f"去重后数据量: {self.stats['dedup_count']}")
        print(f"移除重复数据: {self.stats['removed_count']}")
        print(f"重复率: {self.stats['duplicate_rate']:.2f}%")
        print(f"去重依据列: {self.stats['subset']}")
        print(f"保留策略: {self.stats['keep_strategy']}")
        if 'output_path' in self.stats:
            print(f"输出文件: {self.stats['output_path']}")
        print("=" * 50)

    def find_duplicates(
        self,
        source: Union[pd.DataFrame, str],
        subset: Optional[List[str]] = None,
        keep: str = 'first',
        **kwargs
    ) -> pd.DataFrame:
        df = self._read_data(source, **kwargs)
        mask = df.duplicated(subset=subset, keep=keep)
        return df[mask].copy()

    def get_duplicate_groups(
        self,
        source: Union[pd.DataFrame, str],
        subset: Optional[List[str]] = None,
        **kwargs
    ) -> pd.DataFrame:
        df = self._read_data(source, **kwargs)
        group_cols = subset if subset else list(df.columns)
        dup_mask = df.duplicated(subset=subset, keep=False)
        dup_df = df[dup_mask].copy()

        if not dup_df.empty:
            dup_df = dup_df.sort_values(by=group_cols)
            dup_df['duplicate_group'] = dup_df.groupby(group_cols).ngroup()

        return dup_df
