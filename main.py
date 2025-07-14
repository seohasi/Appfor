import streamlit as st
import plotly.graph_objects as go
import numpy as np

# H-R 다이어그램 배경 데이터 생성 함수
def generate_hr_background():
    # 주계열성
    log_L_ms = np.linspace(-4, 6, 100)  # 광도 범위 (로그 스케일)
    log_T_ms = 3.76 - 0.1 * log_L_ms    # 온도와 광도의 단순 관계
    L_ms = 10 ** log_L_ms
    T_ms = 10 ** log_T_ms

    # 거성
    log_L_giants = np.linspace(1, 4, 50)
    log_T_giants = np.linspace(3.5, 3.7, 50)
    L_giants = 10 ** log_L_giants
    T_giants = 10 ** log_T_giants

    # 백색왜성
    log_L_wd = np.linspace(-4, -1, 50)
    log_T_wd = np.linspace(4, 4.5, 50)
    L_wd = 10 ** log_L_wd
    T_wd = 10 ** log_T_wd

    return L_ms, T_ms, L_giants, T_giants, L_wd, T_wd

# 광도로부터 질량 추정 함수
def estimate_mass(L):
    return L ** (1 / 3.5)  # 주계열성의 질량-광도 관계: M = L^(1/3.5)

# 진화 경로 정의 함수
def define_evolution_path(L, T, M):
    if M < 8:
        # 저질량 별: 주계열성 -> 적색거성 -> 백색왜성
        path = [
            (L, T),             # 주계열성
            (L * 100, T * 0.7), # 적색거성
            (L / 100, T * 1.5)  # 백색왜성
        ]
    else:
        # 고질량 별: 주계열성 -> 초거성 -> 초신성
        path = [
            (L, T),              # 주계열성
            (L * 1000, T * 0.6), # 초거성
            (L * 1000, T * 0.6)  # 초신성 (위치 유지로 표현)
        ]
    return path

# Plotly 그래프 생성 함수
def create_plot(L_ms, T_ms, L_giants, T_giants, L_wd, T_wd, path):
    fig = go.Figure()

    # 배경 데이터 추가
    fig.add_trace(go.Scatter(x=T_ms, y=L_ms, mode='markers', name='주계열성', marker=dict(color='blue', size=5)))
    fig.add_trace(go.Scatter(x=T_giants, y=L_giants, mode='markers', name='거성', marker=dict(color='red', size=5)))
    fig.add_trace(go.Scatter(x=T_wd, y=L_wd, mode='markers', name='백색왜성', marker=dict(color='green', size=5)))

    # 별의 진화 경로 추가
    path_T = [p[1] for p in path]
    path_L = [p[0] for p in path]
    fig.add_trace(go.Scatter(x=path_T, y=path_L, mode='lines+markers', name='진화 경로', line=dict(color='black'), marker=dict(size=10)))

    # 애니메이션 프레임 생성
    frames = []
    for i in range(len(path)):
        frame = go.Frame(data=[go.Scatter(x=[path_T[i]], y=[path_L[i]], mode='markers', marker=dict(color='yellow', size=15))])
        frames.append(frame)

    fig.frames = frames

    # 레이아웃 설정
    fig.update_layout(
        title='H-R 다이어그램과 별의 진화',
        xaxis_title='온도 (K)',
        yaxis_title='광도 (L_sun)',
        xaxis=dict(autorange='reversed', type='log'),  # 온도는 왼쪽에서 오른쪽으로 감소
        yaxis=dict(type='log'),
        updatemenus=[dict(type='buttons', buttons=[dict(label='재생', method='animate', args=[None, dict(frame=dict(duration=1000, redraw=True), fromcurrent=True)])])]
    )

    return fig

# Streamlit 앱
def main():
    st.title("H-R 다이어그램에서 별의 진화 시뮬레이션")

    # 사용자 입력
    st.write("별의 광도와 온도를 입력하세요:")
    L = st.number_input("광도 (태양 광도 단위, L_sun)", min_value=0.0001, max_value=1000000.0, value=1.0)
    T = st.number_input("온도 (켈빈, K)", min_value=1000.0, max_value=50000.0, value=5800.0)

    # 질량 추정
    M = estimate_mass(L)
    st.write(f"추정된 질량: {M:.2f} 태양 질량")

    # 진화 경로 정의
    path = define_evolution_path(L, T, M)

    # 배경 데이터 생성
    L_ms, T_ms, L_giants, T_giants, L_wd, T_wd = generate_hr_background()

    # 그래프 생성 및 표시
    fig = create_plot(L_ms, T_ms, L_giants, T_giants, L_wd, T_wd, path)
    st.plotly_chart(fig)

    # 설명 추가
    st.markdown("""
    ### 설명
    - **주계열성**: 파란색 점으로 표시.
    - **거성**: 빨간색 점으로 표시.
    - **백색왜성**: 초록색 점으로 표시.
    - 입력한 별은 노란색 점으로 표시되며, 검은 선은 진화 경로를 나타냅니다.
    - 질량이 8 태양 질량 미만이면 적색거성을 거쳐 백색왜성으로 진화합니다.
    - 질량이 8 태양 질량 이상이면 초거성을 거쳐 초신성으로 끝납니다.
    """)

if __name__ == "__main__":
    main()
