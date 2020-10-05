mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"diego.serodio@ieee.org\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
