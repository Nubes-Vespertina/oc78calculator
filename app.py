# app.py - 最终部署版本
import streamlit as st
import random
import math
from datetime import datetime

# 配置页面
st.set_page_config(
    page_title="OC78尺寸推算器",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

class OCSizeCalculator:
    def __init__(self):
        self.ethnicity_baselines = {
            "东亚": 13.5, "西欧/北美/澳洲": 14.0, "中东/东欧": 14.5, 
            "中非/西非": 15.0, "全球平均": 14.0
        }
        
        self.reference_objects = {
            "银行卡": 8.56, "智能手机": 14.0, "标准铅笔": 17.5, "易拉罐高度": 12.0,
            "电视遥控器": 16.0, "香蕉（中等）": 18.0, "A4纸短边": 21.0, "一瓶可乐": 23.0,
            "笔记本电脑宽度": 30.0, "小臂长度": 35.0, "标准尺子": 40.0, 
            "大型披萨直径": 45.0, "半米长度": 50.0
        }
    
    def calculate_bmi(self, height_cm, weight_kg):
        height_m = height_cm / 100
        return weight_kg / (height_m ** 2)
    
    def get_fat_pad_reduction(self, bmi):
        if bmi < 18.5: 
            return 0
        elif bmi <= 24.9: 
            return random.uniform(0, 0.5)
        elif bmi <= 29.9: 
            return random.uniform(0.5, 1.5)
        else: 
            return random.uniform(1.5, 3.0)
    
    def generate_hormone_modifier(self, development_quality):
        range_map = {
            "发育迟缓": (0.80, 0.95), 
            "略低于平均": (0.95, 1.00),
            "处于平均范围": (1.00, 1.05), 
            "发育良好": (1.05, 1.10),
            "发育非常充分": (1.10, 1.20), 
            "随机模式": (0.80, 1.20)
        }
        low, high = range_map.get(development_quality, (1.00, 1.05))
        return random.uniform(low, high)
    
    def calculate_height_effect(self, height_cm):
        return max(-0.3, min(0.3, (height_cm - 175) * 0.01))
    
    def calculate_erection_factor(self):
        return random.uniform(1.2, 1.7)
    
    def apply_special_drug_effects(self, base_size, drug_types):
        modifier = 1.0
        if drug_types:
            if "Cobra科技🧪" in drug_types:
                modifier *= random.uniform(1.4, 2.5)
            if "类雌激素🚺" in drug_types:
                modifier *= random.uniform(0.3, 0.7)
        return base_size * modifier
    
    def find_closest_reference(self, length_cm):
        closest_obj, min_diff = None, float('inf')
        for obj, obj_length in self.reference_objects.items():
            diff = abs(length_cm - obj_length)
            if diff < min_diff:
                min_diff, closest_obj = diff, (obj, obj_length)
        return closest_obj
    
    def get_reference_comparison(self, length_cm):
        obj, obj_length = self.find_closest_reference(length_cm)
        difference = length_cm - obj_length
        if abs(difference) < 0.5:
            return f"📏 约等于 {obj} 的长度 ({obj_length}cm)"
        elif difference > 0:
            return f"📏 比 {obj} 长 {difference:.1f}cm"
        else:
            return f"📏 比 {obj} 短 {abs(difference):.1f}cm"
    
    def calculate(self, ethnicity, height_cm, weight_kg, hormone_development, drug_types):
        base_size = self.ethnicity_baselines.get(ethnicity, 14.0)
        adjusted_base = base_size + self.calculate_height_effect(height_cm)
        
        hormone_modifier = self.generate_hormone_modifier(hormone_development)
        flaccid_actual = adjusted_base * hormone_modifier
        flaccid_actual = self.apply_special_drug_effects(flaccid_actual, drug_types)
        
        bmi = self.calculate_bmi(height_cm, weight_kg)
        fat_pad = self.get_fat_pad_reduction(bmi)
        flaccid_visible = max(0, flaccid_actual - fat_pad)
        
        erection_factor = self.calculate_erection_factor()
        erect_length = flaccid_actual * erection_factor
        
        return {
            "疲软实际长度": round(flaccid_actual, 2),
            "疲软显露长度": round(flaccid_visible, 2),
            "勃起长度": round(erect_length, 2),
            "勃起系数": round(erection_factor, 2),
            "激素影响因子": round(hormone_modifier, 3),
            "脂肪垫埋没长度": round(fat_pad, 2),
            "BMI": round(bmi, 1),
            "基础尺寸": round(adjusted_base, 2),
            "疲软实际长度参照": self.get_reference_comparison(flaccid_actual),
            "疲软显露长度参照": self.get_reference_comparison(flaccid_visible),
            "勃起长度参照": self.get_reference_comparison(erect_length),
            "药物信息": f"使用药物: {', '.join(drug_types)}" if drug_types else ""
        }

def init_session_state():
    defaults = {
        'username': '', 'oc_name': '', 'ethnicity': '全球平均',
        'height': 175, 'weight': 70, 'hormone_development': '随机模式',
        'drug_types': [], 'result': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def clear_form():
    for key in ['username', 'oc_name', 'ethnicity', 'height', 'weight', 
                'hormone_development', 'drug_types', 'result']:
        if key in st.session_state:
            if key == 'ethnicity':
                st.session_state[key] = '全球平均'
            elif key == 'height':
                st.session_state[key] = 175
            elif key == 'weight':
                st.session_state[key] = 70
            elif key == 'hormone_development':
                st.session_state[key] = '随机模式'
            elif key == 'drug_types':
                st.session_state[key] = []
            elif key == 'result':
                st.session_state[key] = None
            else:
                st.session_state[key] = ''

def main():
    init_session_state()
    calculator = OCSizeCalculator()
    
    st.title("🎨 OC78尺寸推算器")
    st.markdown("### 基于医学统计模型的娱乐性创作辅助工具")
    
    with st.expander("👤 用户信息", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("创作者名称", key="username", placeholder="可选")
        with col2:
            st.text_input("OC角色名称", key="oc_name", placeholder="可选")
    
    with st.expander("⚠️ 重要声明", expanded=True):
        st.markdown("""
        - **娱乐性质**：仅供OC创作娱乐使用
        - **非医学工具**：结果不具备医学参考价值
        - **个体差异**：请勿将结果与真实人物关联
        - **虚构药物**：Cobra科技🧪和类雌激素🚺为完全虚构物质
        """)
    
    st.header("📝 OC基本信息")
    col1, col2 = st.columns(2)
    
    with col1:
        st.selectbox("种族/族群背景", options=list(calculator.ethnicity_baselines.keys()), key="ethnicity")
        st.slider("身高 (cm)", 140, 220, key="height")
    
    with col2:
        st.slider("体重 (kg)", 40, 150, key="weight")
        bmi = calculator.calculate_bmi(st.session_state.height, st.session_state.weight)
        bmi_cat = "偏瘦" if bmi < 18.5 else "正常" if bmi < 25 else "超重" if bmi < 30 else "肥胖"
        st.metric("BMI指数", f"{bmi:.1f} ({bmi_cat})")
    
    with st.expander("🔧 高级设定", expanded=False):
        col3, col4 = st.columns(2)
        with col3:
            st.radio("激素发育背景", 
                    ["随机模式", "发育迟缓", "略低于平均", "处于平均范围", "发育良好", "发育非常充分"],
                    key="hormone_development")
        
        with col4:
            drug_options = ["Cobra科技🧪", "类雌激素🚺", "睾酮补充剂", "生长激素", "合成类固醇"]
            st.multiselect("药物使用", options=drug_options, key="drug_types")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🎯 开始推算", use_container_width=True):
            result = calculator.calculate(
                st.session_state.ethnicity, st.session_state.height, st.session_state.weight,
                st.session_state.hormone_development, st.session_state.drug_types
            )
            st.session_state.result = result
            st.success("推算完成！")
    
    with col_btn2:
        if st.button("🗑️ 清空数据", use_container_width=True):
            clear_form()
            st.rerun()
    
    if st.session_state.result:
        result = st.session_state.result
        
        user_info = []
        if st.session_state.username: 
            user_info.append(f"创作者: {st.session_state.username}")
        if st.session_state.oc_name: 
            user_info.append(f"角色: {st.session_state.oc_name}")
        if user_info:
            st.info(f"{' | '.join(user_info)} | 时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        st.header("📊 推算结果")
        
        st.subheader("😴 疲软状态")
        col5, col6 = st.columns(2)
        with col5:
            st.metric("实际生物长度", f"{result['疲软实际长度']}cm")
            st.info(result['疲软实际长度参照'])
        with col6:
            st.metric("视觉显露长度", f"{result['疲软显露长度']}cm")
            st.info(result['疲软显露长度参照'])
        
        st.subheader("🚀 勃起状态")
        col7, col8 = st.columns(2)
        with col7:
            st.metric("勃起长度", f"{result['勃起长度']}cm")
            st.info(result['勃起长度参照'])
        with col8:
            growth = result['勃起长度'] - result['疲软实际长度']
            st.metric("勃起增长", f"+{growth:.1f}cm", delta=f"+{(result['勃起系数']-1)*100:.0f}%")
            st.metric("勃起系数", f"{result['勃起系数']}")
        
        st.subheader("🔬 其他指标")
        col9, col10, col11 = st.columns(3)
        with col9: 
            st.metric("基础尺寸", f"{result['基础尺寸']}cm")
        with col10: 
            st.metric("激素影响", f"{result['激素影响因子']}")
        with col11: 
            st.metric("脂肪垫影响", f"-{result['脂肪垫埋没长度']}cm")
        
        if result['药物信息']:
            st.info(result['药物信息'])
        
        with st.expander("💾 结果记录", expanded=False):
            summary = f"""OC78尺寸推算结果
时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
创作者: {st.session_state.username or '未提供'}
角色: {st.session_state.oc_name or '未命名'}

疲软实际长度: {result['疲软实际长度']}cm
疲软显露长度: {result['疲软显露长度']}cm
勃起长度: {result['勃起长度']}cm
勃起系数: {result['勃起系数']}
基础尺寸: {result['基础尺寸']}cm
激素影响因子: {result['激素影响因子']}
脂肪垫埋没: {result['脂肪垫埋没长度']}cm
"""
            st.download_button(
                "📥 下载结果",
                summary,
                f"OC尺寸_{st.session_state.oc_name or '未命名'}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )
    
    st.markdown("---")
    st.markdown("🎨 仅供OC创作娱乐使用 | 📊 基于群体统计学模型 | ⚠️ 不具备医学参考价值")

if __name__ == "__main__":
    main()
