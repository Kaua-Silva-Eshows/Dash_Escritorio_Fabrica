import pandas as pd
import streamlit.components.v1 as components
import streamlit as st

def function_copy_dataframe_as_tsv(df):
    # Converte o DataFrame para uma string TSV
    df_tsv = df.to_csv(index=False, sep='\t')
    
    # Gera código HTML e JavaScript para copiar o conteúdo para a área de transferência
    components.html(
        f"""
        <style>
            .custom-copy-btn {{
                background: linear-gradient(90deg, #8B0000 0%, #A52A2A 100%);
                color: #fff;
                border: none;
                padding: 12px 28px 12px 18px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                display: inline-flex;
                align-items: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.10);
                transition: background 0.3s, color 0.3s;
                position: relative;
                gap: 8px;
            }}
            .custom-copy-btn:hover {{
                background: linear-gradient(90deg, #A52A2A 0%, #8B0000 100%);
                color: #222;
            }}
            .copy-icon {{
                width: 20px;
                height: 20px;
                vertical-align: middle;
                fill: currentColor;
            }}
        </style>
        <textarea id="clipboard-textarea" style="position: absolute; left: -10000px;">{df_tsv}</textarea>
        <button class="custom-copy-btn" id="copy-btn" onclick="copyDF()">
            <svg class='copy-icon' viewBox='0 0 24 24'><path d='M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z'/></svg>
            <span id="copy-btn-text">Copiar DataFrame</span>
        </button>
        <script>
        function copyDF() {{
            var textarea = document.getElementById('clipboard-textarea');
            textarea.select();
            document.execCommand('copy');
            var btn = document.getElementById('copy-btn');
            var btnText = document.getElementById('copy-btn-text');
            btnText.innerText = 'Copiado!';
            btn.style.background = 'linear-gradient(90deg, #4BB543 0%, #43e97b 100%)';
            setTimeout(function() {{
                btnText.innerText = 'Copiar DataFrame';
                btn.style.background = 'linear-gradient(90deg, #8B0000 0%, #A52A2A 100%)';
            }}, 1500);
        }}
        </script>
        """,
        height=110
    )

def function_box_lenDf(len_df, df, y='', x='', box_id='', item='', total_line=False):
    if total_line == True:
        len_df = len(df)
        len_df -= 1
    else:
        len_df = len(df)

    st.markdown(
        """
        <style>
        .small-box {
            border: 1px solid #8B0000; /* Cor da borda */
            border-radius: 5px; /* Cantos arredondados */
            padding: 10px; /* Espaçamento interno */
            background-color: transparent; /* Cor de fundo da caixa */
            box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1); /* Sombra */
            font-size: 14px; /* Tamanho da fonte */
            font-weight: bold; /* Negrito */
            text-align: center; /* Alinhamento do texto */
            width: 150px; /* Largura da caixinha */
            z-index: 1; /* Garantir que a caixa fique acima de outros elementos */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # CSS para o posicionamento específico via ID
    st.markdown(
        f"""
        <style>
        #{box_id} {{
            position: absolute; /* Posicionamento absoluto */
            top: {y}px; /* Distância do topo da página */
            left: {x}px; /* Distância da borda esquerda da página */
        }}
        </style>
        <div id="{box_id}" class="small-box">
            O DataFrame contém <span style="color: #8B0000;">{len_df}</span> {item}.
        </div>
        """,
        unsafe_allow_html=True
    )

def function_format_number_columns(df=None, columns_money=[], columns_number=[], columns_percent=[], valor=None):
    if valor is not None:
        try:
            valor = float(valor)
            return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except (ValueError, TypeError):
            return ""

    # Formatando colunas de DataFrame
    if df is not None:
        if columns_money:
            for column in columns_money:
                if column in df.columns:
                    try:
                        df[column] = pd.to_numeric(df[column])  
                        df[column] = df[column].apply(
                            lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") 
                            if isinstance(x, (int, float)) else x
                        )
                    except Exception:
                        continue

        if columns_number:
            for column in columns_number:
                if column in df.columns:
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce')
                        df[column] = df[column].apply(
                            lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") 
                            if pd.notnull(x) else ''
                        )
                    except Exception:
                        continue

        if columns_percent:
            for column in columns_percent:
                if column in df.columns:
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce')
                        df[column] = df[column].apply(
                            lambda x: f"{x:.2f}%".replace(".", ",") if pd.notnull(x) else ''
                        )
                    except Exception:
                        continue

    return df
    
def function_highlight_percentage(valuer, invert_color=False):
    if valuer == '-' or pd.isnull(valuer):
        return ''
    
    if invert_color == True:
        try:
            valuer_float = float(valuer.replace('%', '').replace('+', '').replace(',', '.'))
            if valuer_float < 0:
                color = 'green'  # Caiu o preço -> verde
            elif valuer_float > 0:
                color = 'red'    # Subiu o preço -> vermelho
            return f'color: {color}'
        except:
            return ''
    else:
        try:
            valuer_float = float(valuer.replace('%', '').replace('+', '').replace(',', '.'))
            if valuer_float < 0:
                color = 'red'    # Caiu o preço -> vermelho
            elif valuer_float > 0:
                color = 'green'  # Subiu o preço -> verde
            return f'color: {color}'
        except:
            return ''

def function_highlight_value(value, invert_color=False):
    if pd.isnull(value) or value == '':
        return ''

    try:
        # Remove 'R$' e formata corretamente para float
        cleaned = value.replace('R$', '').replace('.', '').replace(',', '.').strip()
        number = float(cleaned)

        if invert_color:
            if number < 0:
                return 'color: green'
            elif number > 0:
                return 'color: red'
        else:
            if number < 0:
                return 'color: red'
            elif number > 0:
                return 'color: green'
        return ''
    except Exception:
        return ''
        
def format_brazilian(num):
    if pd.isnull(num):
        return None
    # Primeiro formata no estilo americano
    formatted = f"{num:,.2f}"
    # Depois inverte vírgula e ponto
    formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
    return formatted

def format_columns_brazilian(df, numeric_columns):
    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].apply(format_brazilian)
    return df

def format_date_brazilian(df, date_column):
  df[date_column] = pd.to_datetime(df[date_column])
  df[date_column] = df[date_column].dt.strftime('%d-%m-%Y')
  return df

def function_format_amount(row):
    unidade = str(row['Unidade Medida']).upper()
    if "KG" in unidade:
        return "G"
    elif "L" in unidade:
        return "ML"
    else:
        return unidade

