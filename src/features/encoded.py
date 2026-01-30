import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def encode_train_test(train_df, test_df, target_col="price", max_cardinality=15):
    # Separate target
    y_train = train_df[target_col]
    y_test = test_df[target_col]

    X_train = train_df.drop(columns=target_col)
    X_test = test_df.drop(columns=target_col)

    # Detect categorical columns
    cat_cols = X_train.select_dtypes(include="object").columns.tolist()

    # Drop high-cardinality categoricals 
    low_card_cols = [
        col for col in cat_cols
        if X_train[col].nunique() <= max_cardinality
    ]

    drop_cols = list(set(cat_cols) - set(low_card_cols))

    # Numerical columns 
    num_cols = X_train.drop(columns=cat_cols).columns.tolist()

    encoder = OneHotEncoder(
        sparse_output=False,
        handle_unknown="ignore"
    )

    # Encode
    X_train_cat = encoder.fit_transform(X_train[low_card_cols])
    X_test_cat = encoder.transform(X_test[low_card_cols])

    cat_feature_names = encoder.get_feature_names_out(low_card_cols)

    X_train_cat = pd.DataFrame(X_train_cat, columns=cat_feature_names)
    X_test_cat = pd.DataFrame(X_test_cat, columns=cat_feature_names)

    X_train_num = X_train[num_cols].reset_index(drop=True)
    X_test_num = X_test[num_cols].reset_index(drop=True)

    X_train_final = pd.concat([X_train_num, X_train_cat], axis=1)
    X_test_final = pd.concat([X_test_num, X_test_cat], axis=1)

    return X_train_final, X_test_final, y_train, y_test
