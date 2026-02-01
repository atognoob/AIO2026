import time
import io
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Linear Regression (GD)", layout="wide")

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 3rem; }
    .kpi-card {
        padding: 1rem 1.2rem;
        border-radius: 14px;
        background: #f8f9fb;
        border: 1px solid #e9ecf1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Linear Regression Dashboard")
st.caption("Gradient Descent training with interactive data prep and analysis.")

def train_test_split(X, y, test_size=0.2, seed=42):
    np.random.seed(seed)
    idx = np.arange(len(X))
    np.random.shuffle(idx)
    split = int(len(X) * (1 - test_size))
    train_idx, test_idx = idx[:split], idx[split:]
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]

def standardize_fit(X):
    mu = X.mean(axis=0)
    sigma = X.std(axis=0) + 1e-12
    return mu, sigma

def standardize_transform(X, mu, sigma):
    return (X - mu) / sigma

def mse(y, y_pred):
    return np.mean((y - y_pred) ** 2)

def rmse(y, y_pred):
    return np.sqrt(mse(y, y_pred))

def mae(y, y_pred):
    return np.mean(np.abs(y - y_pred))

def r2_score(y, y_pred):
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    return 1 - (ss_res / (ss_tot + 1e-12))

def add_bias(X):
    return np.c_[np.ones((X.shape[0], 1)), X]

def linear_regression_gd(X, y, lr=0.05, epochs=8000, tol=1e-8):
    Xb = add_bias(X)
    n, d = Xb.shape
    w = np.zeros(d)
    loss_history = []
    prev_loss = float("inf")
    start = time.time()
    for epoch in range(epochs):
        y_pred = Xb @ w
        error = y_pred - y
        grad = (2 / n) * (Xb.T @ error)
        w -= lr * grad
        loss = mse(y, y_pred)
        loss_history.append(loss)
        if abs(prev_loss - loss) < tol:
            break
        prev_loss = loss
    train_time = time.time() - start
    return w, loss_history, epoch + 1, train_time

def predict(X, w):
    Xb = add_bias(X)
    return Xb @ w

def prepare_data(df, target, feature_cols, missing):
    data = df.copy()
    before_rows = len(data)

    if missing == "drop rows":
        data = data.dropna()
    else:
        for col in data.columns:
            if pd.api.types.is_numeric_dtype(data[col]):
                data[col] = data[col].fillna(data[col].mean())
        data = data.dropna()

    dropped_rows = before_rows - len(data)

    if target not in data.columns:
        return None, None, "Target column not found.", dropped_rows

    if not feature_cols:
        return None, None, "No feature columns selected.", dropped_rows

    if not pd.api.types.is_numeric_dtype(data[target]):
        return None, None, "Target column must be numeric.", dropped_rows

    y = data[target].values
    X_raw = data[feature_cols].copy()
    cat_cols = [c for c in X_raw.columns if not pd.api.types.is_numeric_dtype(X_raw[c])]
    cat_maps = {}

    if cat_cols:
        for col in cat_cols:
            cat = pd.Categorical(X_raw[col])
            cat_maps[col] = list(cat.categories)
            X_raw[col] = cat.codes

    return X_raw, y, None, dropped_rows, data, cat_cols, cat_maps

def missing_summary(df_in):
    missing = df_in.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    if missing.empty:
        return None
    return pd.DataFrame({"column": missing.index, "missing": missing.values})

uploaded = st.file_uploader("Upload CSV", type=["csv"])
if uploaded is not None:
    df = pd.read_csv(uploaded)
else:
    df = None

if df is None:
    st.info("Upload a CSV file to continue.")
    st.stop()

tabs = st.tabs(["Data", "Training", "Results", "Predict"])

with st.sidebar:
    st.header("Configuration")
    columns = list(df.columns)
    target_col = st.selectbox("Target column", options=columns)
    feature_options = [c for c in columns if c != target_col]
    feature_cols = st.multiselect(
        "Feature columns (tick to train)",
        options=feature_options,
        default=feature_options,
    )
    missing_strategy = st.selectbox(
        "Missing values",
        ["drop rows", "fill with mean"],
        index=0,
    )

    st.header("Training")
    test_size = st.slider("Test size", 0.1, 0.4, 0.2, 0.05)
    seed = st.number_input("Random seed", value=42, step=1)
    lr = st.number_input("Learning rate", value=0.05, step=0.01, format="%.4f")
    epochs = st.number_input("Epochs", value=8000, step=100)
    tol = st.number_input("Tolerance", value=1e-8, format="%.1e")

X_df, y, err, dropped_rows, data_clean, cat_cols, cat_maps = prepare_data(
    df, target_col, feature_cols, missing_strategy
)
if err:
    st.error(err)
    st.stop()
if len(X_df) < 5:
    st.error("Not enough data after preprocessing.")
    st.stop()

feature_names = list(X_df.columns)
X = X_df.values.astype(float)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size, seed=int(seed)
)

mu, sigma = standardize_fit(X_train)
X_train_mu = standardize_transform(X_train, mu, sigma)
X_test_mu = standardize_transform(X_test, mu, sigma)

def make_signature(df_in, target, features, missing, test_size, seed, lr, epochs, tol):
    return {
        "rows": len(df_in),
        "cols": list(df_in.columns),
        "target": target,
        "features": list(features),
        "missing": missing,
        "test_size": float(test_size),
        "seed": int(seed),
        "lr": float(lr),
        "epochs": int(epochs),
        "tol": float(tol),
    }

if "results" not in st.session_state:
    st.session_state.results = None
if "signature" not in st.session_state:
    st.session_state.signature = None

signature = make_signature(
    df, target_col, feature_cols, missing_strategy, test_size, seed, lr, epochs, tol
)

if st.session_state.results is None or st.session_state.signature != signature:
    w, loss_history, n_epochs, train_time = linear_regression_gd(
        X_train_mu, y_train, lr=lr, epochs=int(epochs), tol=tol
    )
    y_train_pred = predict(X_train_mu, w)
    y_test_pred = predict(X_test_mu, w)
    st.session_state.results = {
        "w": w,
        "loss_history": loss_history,
        "n_epochs": n_epochs,
        "train_time": train_time,
        "y_train_pred": y_train_pred,
        "y_test_pred": y_test_pred,
        "y_test": y_test,
        "cat_maps": cat_maps,
    }
    st.session_state.signature = signature

res = st.session_state.results

with tabs[0]:
    st.subheader("Dataset Overview", anchor=False)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(
            '<div class="kpi-card">Rows<br><b>{}</b></div>'.format(len(df)),
            unsafe_allow_html=True,
        )
    with col_b:
        st.markdown(
            '<div class="kpi-card">Columns<br><b>{}</b></div>'.format(len(df.columns)),
            unsafe_allow_html=True,
        )
    with col_c:
        st.markdown(
            '<div class="kpi-card">Selected Features<br><b>{}</b></div>'.format(
                len(feature_names)
            ),
            unsafe_allow_html=True,
        )

    st.markdown("### Preview", unsafe_allow_html=True)
    st.dataframe(df.head(12), use_container_width=True)

    if dropped_rows > 0:
        st.warning(f"Dropped {dropped_rows} rows due to missing values.")

    st.markdown("### Data Describe", unsafe_allow_html=True)
    st.dataframe(df.describe(include="all").transpose(), use_container_width=True)

    st.markdown("### Data Info", unsafe_allow_html=True)
    info_buf = io.StringIO()
    df.info(buf=info_buf)
    st.text(info_buf.getvalue())

    miss = missing_summary(df)
    if miss is not None:
        st.markdown("### Missing Values", unsafe_allow_html=True)
        st.bar_chart(miss.set_index("column"))

    numeric_df = df.select_dtypes(include=[np.number])
    if not numeric_df.empty:
        st.markdown("### Correlation (numeric)", unsafe_allow_html=True)
        st.dataframe(numeric_df.corr(), use_container_width=True)

with tabs[1]:
    st.subheader("Training Summary", anchor=False)
    st.write(
        {
            "Training time (s)": round(res["train_time"], 4),
            "Epochs": res["n_epochs"],
            "Features": len(feature_names),
            "Train rows": len(X_train),
            "Test rows": len(X_test),
        }
    )

    st.markdown("### Loss Curve", unsafe_allow_html=True)
    st.line_chart(pd.DataFrame({"loss": res["loss_history"]}))

with tabs[2]:
    st.subheader("Model Performance", anchor=False)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Train R2", f"{r2_score(y_train, res['y_train_pred']):.4f}")
    c2.metric("Test R2", f"{r2_score(y_test, res['y_test_pred']):.4f}")
    c3.metric("Train RMSE", f"{rmse(y_train, res['y_train_pred']):.4f}")
    c4.metric("Test RMSE", f"{rmse(y_test, res['y_test_pred']):.4f}")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Train Metrics", unsafe_allow_html=True)
        st.write(
            {
                "MSE": mse(y_train, res["y_train_pred"]),
                "RMSE": rmse(y_train, res["y_train_pred"]),
                "MAE": mae(y_train, res["y_train_pred"]),
                "R2": r2_score(y_train, res["y_train_pred"]),
            }
        )
    with col2:
        st.markdown("### Test Metrics", unsafe_allow_html=True)
        st.write(
            {
                "MSE": mse(y_test, res["y_test_pred"]),
                "RMSE": rmse(y_test, res["y_test_pred"]),
                "MAE": mae(y_test, res["y_test_pred"]),
                "R2": r2_score(y_test, res["y_test_pred"]),
            }
        )

    st.markdown("### Predicted vs Actual (Test)", unsafe_allow_html=True)
    pred_df = pd.DataFrame(
        {
            "actual": res["y_test"],
            "predicted": res["y_test_pred"],
        }
    )
    st.scatter_chart(pred_df, x="actual", y="predicted")

    st.markdown("### Weights", unsafe_allow_html=True)
    weights_df = pd.DataFrame(
        {
            "feature": ["bias"] + feature_names,
            "weight": res["w"],
        }
    )
    st.dataframe(weights_df, use_container_width=True)

    st.download_button(
        "Download test predictions (CSV)",
        data=pred_df.to_csv(index=False).encode("utf-8"),
        file_name="test_predictions.csv",
        mime="text/csv",
    )

with tabs[3]:
    st.subheader("Single Prediction", anchor=False)
    with st.form("predict_form"):
        inputs = {}
        for name in feature_cols:
            if name in cat_cols:
                options = res["cat_maps"].get(name, [])
                if options:
                    val = st.selectbox(name, options=options)
                else:
                    val = st.text_input(name, value="")
            else:
                val = st.number_input(name, value=0.0, format="%.4f")
            inputs[name] = val
        submitted = st.form_submit_button("Predict")

    if submitted:
        input_df = pd.DataFrame([inputs])
        for col in cat_cols:
            categories = res["cat_maps"].get(col, [])
            if categories:
                if input_df.loc[0, col] not in categories:
                    st.error(f"Value '{input_df.loc[0, col]}' not seen in training for {col}.")
                    st.stop()
                input_df[col] = pd.Categorical(input_df[col], categories=categories).codes

        x = input_df[feature_names].values.astype(float)
        x_mu = standardize_transform(x, mu, sigma)
        y_pred = predict(x_mu, res["w"])[0]
        st.success(f"Predicted {target_col}: {y_pred:.4f}")


