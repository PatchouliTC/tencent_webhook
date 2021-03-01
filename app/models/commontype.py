import enum


class HookKind(str,enum.Enum):
    Push='push',
    Merge='merge_request'

    @staticmethod
    def from_str(label):
        if label in ('push',):
            return HookKind.Push
        elif label in ('merge)request'):
            return HookKind.Merge
        else:
            raise ValueError(f"{label} is not support")
