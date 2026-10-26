from pathlib import Path
from streamlit.testing.v1 import AppTest
app=Path(__file__).resolve().parents[1]/'streamlit_app.py'

def test_all_pages_and_role_kits_render():
    at=AppTest.from_file(str(app),default_timeout=15).run()
    assert not at.exception
    pages=list(at.sidebar.radio[0].options)
    for p in pages:
        at.sidebar.radio[0].set_value(p).run()
        assert not at.exception, str(at.exception)
        if 'Intake' in p or 'Structured' in p:
            for role in at.selectbox[0].options:
                at.selectbox[0].set_value(role).run()
                assert not at.exception
    at.sidebar.radio[0].set_value(pages[2]).run()
    at.text_input[0].set_value('no matching background').run()
    assert not at.exception
