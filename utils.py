import pandas as pd

def calcular_faltantes(inventory: pd.DataFrame, set_parts: pd.DataFrame) -> pd.DataFrame:
    # Asegurar columnas
    for col in ["part_num", "color_id", "qty_have"]:
        if col not in inventory.columns:
            raise ValueError(f"Falta columna en inventory: {col}")
    for col in ["set_num", "part_num", "color_id", "qty_required"]:
        if col not in set_parts.columns:
            raise ValueError(f"Falta columna en set_parts: {col}")
    df = set_parts.merge(inventory, on=["part_num","color_id"], how="left")
    df["qty_have"] = df["qty_have"].fillna(0).astype(int)
    df["qty_required"] = df["qty_required"].fillna(0).astype(int)
    df["qty_missing"] = (df["qty_required"] - df["qty_have"]).clip(lower=0)
    return df

def progreso_por_set(sets: pd.DataFrame, set_parts: pd.DataFrame, inventory: pd.DataFrame) -> pd.DataFrame:
    falt = calcular_faltantes(inventory, set_parts)
    agg = falt.groupby("set_num").agg(
        required=("qty_required","sum"),
        missing=("qty_missing","sum")
    ).reset_index()
    agg["have"] = agg["required"] - agg["missing"]
    agg["progress"] = (agg["have"] / agg["required"]).fillna(0.0)
    out = sets.merge(agg, on="set_num", how="left")
    out[["required","missing","have","progress"]] = out[["required","missing","have","progress"]].fillna(0)
    return out

def ensure_dtypes(df: pd.DataFrame, int_cols=None) -> pd.DataFrame:
    int_cols = int_cols or []
    for c in int_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)
    return df
