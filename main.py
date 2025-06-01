import random
import time
import json
import shutil
import os
from datetime import datetime
from colorama import Fore, Style

# ========== 数据模型 ==========
class Asset:
    def __init__(self, code, name, base_price, volatility, income):
        self.code = code
        self.name = name
        # 基础价格确保是数字且有效
        self.base_price = float(max(base_price, 10000))
        self.current_price = self.base_price
        self.volatility = volatility
        self.income = income
        self.history = []  # 列表记录日期和价格字典
        self.operation_history = []  # 新增操作记录

class Bond:
    def __init__(self, code, name, price, yield_rate, duration):
        self.code = code
        self.name = name
        # 价格确保是数字且有效
        self.price = float(max(price, 5000))
        self.current_price = self.price
        self.yield_rate = yield_rate
        self.duration = duration
        self.history = []  # 列表记录日期和价格字典
        self.operation_history = []  # 新增操作记录

    def update_price(self):
        """债券价格波动（带价格保护） - 价格历史记录移至 FinancialMarket"""
        # self.current_price = float(self.current_price * random.uniform(0.98, 1.02))
        # self.current_price = max(self.current_price, 5000.0) # 确保是浮点数比较
        # 价格波动和历史记录处理移至 FinancialMarket.update_bonds
        pass # 价格更新逻辑在 FinancialMarket 中实现

# ========== 游戏系统 ==========
class SeasonSystem:
    SEASONS = [
        {"name": "春", "stock_vol": 1.2, "bond_yield": 0.95},
        {"name": "夏", "stock_vol": 1.5, "bond_yield": 1.0},
        {"name": "秋", "stock_vol": 0.8, "bond_yield": 1.1},
        {"name": "冬", "stock_vol": 1.0, "bond_yield": 1.05}
    ]

    def __init__(self):
        # self.start_day = datetime.now().toordinal() # 使用游戏内天数模拟季节
        pass

    def current_season(self, day):
        """根据游戏天数返回当前季节"""
        return self.SEASONS[day // 7 % 4]

class FinancialMarket:
    def __init__(self):
        self.stocks = self.generate_random_stocks()
        self.bonds = [Bond("GOV01", "国债-3月期", round(random.uniform(0.5, 1.5), 2), 0.03, 90),
                      Bond("GOV02", "国债-1年期", round(random.uniform(9.0, 11.0), 2), 0.035, 365)] # 确保初始价格为浮点数
        self.stock_dict = {s.code: s for s in self.stocks}
        self.bond_dict = {b.code: b for b in self.bonds}
        self.day = 0

    def set_day(self, day):
        self.day = day

    def generate_random_stocks(self):
        """随机生成股票数据"""
        stock_templates = [
            ("APLE", "平果", 0.12, 300), # Apple -> 平果
            ("GGLE", "古歌", 0.15, 400), # Google -> 古歌
            ("HUAW", "化为", 0.18, 280), # Huawei -> 化为
            ("XIAM", "肖米", 0.2, 150), # Xiaomi -> 肖米
            ("HONR", "容耀", 0.22, 180), # Honor -> 容耀
            ("FSSC", "富士糠", 0.16, 250), # Fujitsu -> 富士糠
            ("META", "麦塔", 0.25, 350), # Meta -> 麦塔
            ("CGPT", "拆既", 0.3, 500), # ChatGPT -> 拆既
            ("TWTE", "退特", 0.28, 320), # Twitter -> 退特
            ("VANK", "晚科", 0.2, 200), # Vanke -> 晚科
            ("AMZN", "亚逊", 0.17, 380), # Amazon -> 亚逊
            ("TSLA", "特士拉", 0.28, 250), # Tesla -> 特士拉
            ("MSFT", "威软", 0.14, 320), # Microsoft -> 威软
            ("NFLX", "网飞", 0.21, 280), # Netflix -> 网飞
            ("NVDA", "英伟", 0.35, 550), # NVIDIA -> 英伟
            ("BABA", "阿狸", 0.19, 220), # Alibaba -> 阿狸
            ("TCEH", "藤讯", 0.20, 270), # Tencent -> 藤讯
            ("PYPL", "贝宝付", 0.15, 180), # PayPal -> 贝宝付
            ("ADBE", "奥多比", 0.13, 300),  # Adobe -> 奥多比
            ("COST", "好市客", 0.11, 220), # Costco -> 好市客
            ("CSCO", "思科", 0.09, 180), # Cisco -> 思科
            ("INTC", "英特尔", 0.12, 210), # Intel -> 英特尔
            ("PEPI", "百事", 0.07, 160), # PepsiCo -> 百事
            ("QCOM", "高通", 0.18, 250), # Qualcomm -> 高通
            ("SBUX", "星巴克", 0.14, 190), # Starbucks -> 星巴克
            ("BKNG", "缤客", 0.22, 450), # Booking Holdings -> 缤客
            ("TMUS", "特大", 0.19, 280), # T-Mobile US -> 特大
            ("AMDS", "超微", 0.30, 350), # AMD -> 超微
            ("SUPE", "超微电脑", 0.40, 600) # Super Micro Computer -> 超微电脑
        ]
        stocks = []
        for code, name, vol, income in stock_templates:
            # 根据波动性设置不同的基础价格范围
            if vol >= 0.25:
                # 小型公司 (3000-7999)
                base_price = round(random.uniform(3000.0, 7999.0), 2)
            elif vol >= 0.15 and vol < 0.25:
                # 中型公司 (7000-9999)
                base_price = round(random.uniform(7000.0, 9999.0), 2)
            else:
                # 大型公司 (10000-15999)
                base_price = round(random.uniform(10000.0, 15999.0), 2)

            # 确保基础价格有效
            base_price = float(max(base_price, 3000.0)) # 确保价格不低于最低范围的下限
            stocks.append(Asset(code, name, base_price, vol, income))
        return stocks

    def update_stocks(self, season_mod, current_day):
        """更新股票价格（带波动限制和价格保护）"""
        for stock in self.stocks:
            # 计算基础波动
            base_change = random.gauss(0, 1) * stock.volatility * season_mod

            # 限制波动幅度在±50%之间
            clamped_change = max(min(base_change, 0.5), -0.5)

            # 计算新价格，确保是浮点数运算
            new_price = stock.current_price * (1.0 + clamped_change)
            new_price = float(int(new_price)) # 保持价格为整数元，但存储为浮点以便计算

            # 价格保护：不低于基准价的20%，确保是浮点数比较
            price_floor = stock.base_price * 0.2
            stock.current_price = max(new_price, price_floor)

            # 维护价格历史
            stock.history.append({
                "day": current_day,
                "price": stock.current_price
            })
            if len(stock.history) > 365:  # 保留一年数据
                stock.history.pop(0)

    def update_bonds(self, season_mod, current_day):
        for bond in self.bonds:
            # 债券价格波动（带价格保护）
            change = random.gauss(0, 0.05) * season_mod["bond_yield"]
            new_price = bond.current_price * (1.0 + change) # 确保浮点数运算
            new_price = float(int(new_price)) # 保持价格为整数元
            bond.current_price = max(new_price, 5000.0) # 确保浮点数比较
            # 维护价格历史
            bond.history.append({
                "day": current_day,
                "price": bond.current_price
            })
            if len(bond.history) > 365:
                bond.history.pop(0)

# ========== 核心游戏类 ==========
class StockTycoon:
    def __init__(self, save_name='default_save.json'):
        self.current_save = save_name
        self.player = {
            "cash": 10_000_000_000_000.0,
            "debt": 1_000_000_000_000.0,
            "stocks": {},
            "bonds": {},
            "shorts": {},
            "level": 1,  # 新增等级属性
            "exp": 0,    # 新增经验属性
            "exp_to_next_level": 100  # 升级所需经验
        }
        self.market = FinancialMarket()
        self.season = SeasonSystem()
        self.day = 0
        self.total_assets_history = []
        self.trade_history = []
        self.stocks_bonds_value_history = []
        self.tycoon_mode = False
        self.load_game()
        self.market.set_day(self.day)

    def toggle_tycoon_mode(self):
        """切换土豪模式状态"""
        self.tycoon_mode = not self.tycoon_mode
        print(f"土豪模式已{'开启' if self.tycoon_mode else '关闭'}")
        self.save_game()

    def validate_tycoon_purchase(self, amount):
        """验证土豪模式下的购买数量"""
        if self.tycoon_mode and amount < 1000:
            print(f"{Fore.RED}土豪模式下必须购买1000股或以上！{Style.RESET_ALL}")
            return False
        return True

    def load_game(self):
        """根据当前存档名称加载游戏"""
        filepath = os.path.join('saves', self.current_save)
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                # 加载基础数据
                self.player["cash"] = float(data.get("player", {}).get("cash", self.player["cash"])) if isinstance(data.get("player", {}).get("cash", self.player["cash"]), (int, float)) else 0.0
                self.player["debt"] = float(data.get("player", {}).get("debt", self.player["debt"])) if isinstance(data.get("player", {}).get("debt", self.player["debt"]), (int, float)) else 0.0
                # 加载等级和经验
                self.player["level"] = int(data.get("player", {}).get("level", 1))
                self.player["exp"] = int(data.get("player", {}).get("exp", 0))
                self.player["exp_to_next_level"] = int(data.get("player", {}).get("exp_to_next_level", 100))
                # 持仓信息，确保是字典，并加载包含平均成本的数据结构
                loaded_stocks = data.get("player", {}).get("stocks", {})
                if isinstance(loaded_stocks, dict):
                     # 确保加载的持仓数据格式正确
                     self.player["stocks"] = {
                         code: {"amount": float(h.get("amount", 0.0)), "avg_price": float(h.get("avg_price", 0.0))}
                         for code, h in loaded_stocks.items() if isinstance(h, dict)
                     }
                else:
                     self.player["stocks"] = {} # 如果加载数据格式错误，则初始化为空字典

                loaded_bonds = data.get("player", {}).get("bonds", {})
                if isinstance(loaded_bonds, dict):
                     # 确保加载的持仓数据格式正确
                     self.player["bonds"] = {
                         code: {"amount": float(h.get("amount", 0.0)), "avg_price": float(h.get("avg_price", 0.0))}
                         for code, h in loaded_bonds.items() if isinstance(h, dict)
                     }
                else:
                    self.player["bonds"] = {} # 如果加载数据格式错误，则初始化为空字典


                # 做空持仓 {代码: [数量(float), 借入价格(float), 借入天数(int)]}
                loaded_shorts = data.get("player", {}).get("shorts", {})
                if isinstance(loaded_shorts, dict):
                     # 确保加载的做空数据格式正确
                     self.player["shorts"] = {
                         code: [float(d[0]) if len(d) > 0 and isinstance(d[0], (int, float)) else 0.0, # 数量
                                float(d[1]) if len(d) > 1 and isinstance(d[1], (int, float)) else 0.0, # 借入价格
                                int(d[2]) if len(d) > 2 and isinstance(d[2], (int, float)) else 0] # 借入天数
                         for code, d in loaded_shorts.items() if isinstance(d, list) and len(d) >= 2
                     }
                else:
                     self.player["shorts"] = {} # 如果加载数据格式错误，则初始化为空字典

                self.day = int(data.get("day", 0))
                # 确保加载的历史记录是列表
                self.trade_history = data.get("trade_history", [])
                if not isinstance(self.trade_history, list): self.trade_history = []

                self.total_assets_history = data.get("total_assets_history", []) # 加载总资产历史
                if not isinstance(self.total_assets_history, list): self.total_assets_history = []

                # 加载股票+债券总价值历史
                self.stocks_bonds_value_history = data.get("stocks_bonds_value_history", [])
                if not isinstance(self.stocks_bonds_value_history, list): self.stocks_bonds_value_history = []


                # 加载市场数据
                market_data = data.get("market", {})
                # 加载股票数据
                # 需要先生成默认市场数据，再用存档覆盖历史记录等
                # self.market = FinancialMarket() # 不在这里重新初始化市场
                for stock_data in market_data.get("stocks", []):
                    stock = self.market.stock_dict.get(stock_data.get("code")) # 使用.get避免KeyError
                    if stock:
                        # stock.base_price = float(stock_data.get("base_price", stock.base_price)) # 基础价格不应该从存档加载
                        # 确保加载的历史和操作历史是列表
                        stock.history = stock_data.get("history", [])
                        if not isinstance(stock.history, list): stock.history = []
                        stock.operation_history = stock_data.get("operations", [])
                        if not isinstance(stock.operation_history, list): stock.operation_history = []

                        # 从历史记录中恢复当前价格，确保是浮点数
                        stock.current_price = float(stock.history[-1].get("price", stock.base_price)) if stock.history and isinstance(stock.history[-1], dict) and isinstance(stock.history[-1].get("price"), (int, float)) else float(stock.base_price)

                # 加载债券数据
                for bond_data in market_data.get("bonds", []):
                    bond = self.market.bond_dict.get(bond_data.get("code")) # 使用.get避免KeyError
                    if bond:
                        # bond.price = float(bond_data.get("price", bond.price)) # 基础价格不应该从存档加载
                         # 确保加载的历史和操作历史是列表
                        bond.history = bond_data.get("history", [])
                        if not isinstance(bond.history, list): bond.history = []
                        bond.operation_history = bond_data.get("operations", [])
                        if not isinstance(bond.operation_history, list): bond.operation_history = []

                         # 从历史记录中恢复当前价格，确保是浮点数
                        bond.current_price = float(bond.history[-1].get("price", bond.price)) if bond.history and isinstance(bond.history[-1], dict) and isinstance(bond.history[-1].get("price"), (int, float)) else float(bond.price)

            print(f"{Fore.GREEN}存档加载成功！{Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"新建存档 {self.current_save}，使用默认值开始游戏")
        except json.JSONDecodeError:
             print("存档文件损坏，使用默认值开始游戏")
        except Exception as e:
            print(f"{Fore.RED}存档加载失败：{str(e)}{Style.RESET_ALL}")

    def save_game(self):
        """保存到当前存档文件"""
        data = {
            "player": {
                "cash": self.player["cash"],
                "debt": self.player["debt"],
                "stocks": self.player["stocks"],
                "bonds": self.player["bonds"],
                "shorts": self.player["shorts"],
                "level": self.player["level"],  # 保存等级
                "exp": self.player["exp"],      # 保存经验
                "exp_to_next_level": self.player["exp_to_next_level"]  # 保存升级所需经验
            },
            "day": self.day,
            "trade_history": self.trade_history,
            "total_assets_history": self.total_assets_history, # 保存总资产历史
            "stocks_bonds_value_history": self.stocks_bonds_value_history, # 保存股票+债券总价值历史
            "market": {
                "stocks": [{
                    "code": s.code,
                    "base_price": s.base_price,
                    "volatility": s.volatility, # 保存波动性和收益以便读档时完整恢复
                    "income": s.income,
                    "history": s.history,
                    "operations": s.operation_history
                } for s in self.market.stocks],
                "bonds": [{
                    "code": b.code,
                    "price": b.price,
                    "yield_rate": b.yield_rate, # 保存收益率和期限以便读档时完整恢复
                    "duration": b.duration,
                    "history": b.history,
                    "operations": b.operation_history
                } for b in self.market.bonds]
            }
        }
        filepath = os.path.join('saves', self.current_save)
        try:
            if not os.path.exists('saves'):
                os.makedirs('saves')
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            print("游戏进度已保存")
        except Exception as e:
             print(f"{Fore.RED}存档保存失败：{str(e)}{Style.RESET_ALL}")


    def calculate_total_assets(self):
        """计算玩家总资产"""
        # 确保从player字典获取的值是数字类型，默认为0.0
        cash = self.player.get('cash')
        total = float(cash) if isinstance(cash, (int, float)) else 0.0
        # 计算股票价值
        stocks_dict = self.player.get('stocks', {})
        # 确保stocks_dict是字典类型，避免.items()错误
        if isinstance(stocks_dict, dict):
            for code, holding_data in stocks_dict.items():
                if isinstance(holding_data, dict) and isinstance(holding_data.get("amount"), (int, float)):
                    stock = self.market.stock_dict.get(code)
                    if stock:
                        total += float(stock.current_price) * float(holding_data["amount"])
        # 计算债券价值
        bonds_dict = self.player.get('bonds', {})
        if isinstance(bonds_dict, dict):
            for code, holding_data in bonds_dict.items():
                if isinstance(holding_data, dict) and isinstance(holding_data.get("amount"), (int, float)):
                    bond = self.market.bond_dict.get(code)
                    if bond:
                        total += float(bond.current_price) * float(holding_data["amount"])
        return total

    def show_stock_market(self):
        """显示股票市场信息"""
        print(f"{Fore.CYAN}=== 股票市场 ==={Style.RESET_ALL}")
        print(f"当前第 {self.day} 天")
        # 使用游戏天数获取季节
        season = self.season.current_season(self.day)
        print(f"当前季节：{season['name']} (股票波动：{season['stock_vol']:.1f}x)")
        # 价格显示单位修正为元
        print("代码 | 名称 | 当前价格(元) | 波动性")
        print("-" * 40)
        for stock in self.market.stocks:
            price_yuan = stock.current_price
            print(f"{stock.code} | {stock.name} | {price_yuan:.2f} | {stock.volatility:.2f}") # 格式化价格为2位小数

    def show_bond_market(self):
        """显示债券市场信息"""
        print(f"{Fore.CYAN}=== 债券市场 ==={Style.RESET_ALL}")
        print(f"当前第 {self.day} 天")
         # 使用游戏天数获取季节
        season = self.season.current_season(self.day)
        print(f"当前季节：{season['name']} (债券收益：{season['bond_yield']:.1f}x)")
        # 价格显示单位修正为元
        print("代码 | 名称 | 当前价格(元) | 年化收益率 | 期限(天)")
        print("-" * 50)
        for bond in self.market.bonds:
            price_yuan = bond.current_price
            yield_pct = bond.yield_rate * 100
            print(f"{bond.code} | {bond.name} | {price_yuan:.2f} | {yield_pct:.1f}% | {bond.duration}") # 格式化价格为2位小数

    def buy_bonds(self):
        """购买债券"""
        code = input("请输入债券代码：").upper()
        bond = self.market.bond_dict.get(code)
        if not bond:
            print("无效的债券代码")
            return

        try:
            amount = int(input("请输入购买数量："))
            if amount <= 0:
                raise ValueError("数量必须大于0")
            amount = float(amount)
            # 验证土豪模式
            if not self.validate_tycoon_purchase(amount):
                return
        except ValueError:
            print("无效的数量")
            return

        total_cost = bond.current_price * amount
        cash = self.player.get('cash')
        current_cash = float(cash) if isinstance(cash, (int, float)) else 0.0
        if total_cost > current_cash:
            print("资金不足")
            return

        self.player['cash'] = current_cash - total_cost
        bonds = self.player.get('bonds', {})
        if not isinstance(bonds, dict):
            bonds = {}

        if code in bonds and isinstance(bonds[code], dict):
            existing_amount = float(bonds[code].get("amount", 0.0))
            existing_avg_price = float(bonds[code].get("avg_price", 0.0))
            new_total_amount = existing_amount + amount
            new_avg_price = ((existing_avg_price * existing_amount) + (bond.current_price * amount)) / new_total_amount if new_total_amount > 0 else 0.0
            bonds[code] = {"amount": new_total_amount, "avg_price": new_avg_price}
        else:
            bonds[code] = {"amount": amount, "avg_price": bond.current_price}

        self.player['bonds'] = bonds
        print(f"成功购买 {int(amount)} 单位 {bond.name}")
        bond.operation_history.append({
            "day": self.day,
            "action": "买入",
            "amount": int(amount),
            "price": bond.current_price
        })
        self.record_trade("债券", code, "买入", amount, bond.current_price)
        self.add_exp(10)  # 购买债券增加10点经验
        self.save_game()

    def sell_bonds(self):
        """卖出债券功能"""
        print(f"{Fore.CYAN}=== 债券卖出 ==={Style.RESET_ALL}")
        code = input("请输入要卖出的债券代码：").upper()
        bond = self.market.bond_dict.get(code)

        if not bond:
            print(f"{Fore.RED}错误：无效的债券代码{Style.RESET_ALL}")
            return

        # 获取持仓信息
        bonds = self.player.get("bonds", {})
        if not isinstance(bonds, dict) or code not in bonds or not isinstance(bonds[code], dict) or "amount" not in bonds[code]:
             print(f"{Fore.RED}错误：没有该债券持仓或数据异常{Style.RESET_ALL}")
             return

        holding_data = bonds[code]
        current_amount = float(holding_data.get("amount", 0.0)) # 确保持仓数量是浮点数
        avg_price = float(holding_data.get("avg_price", 0.0)) # 确保平均成本价是浮点数

        if current_amount <= 0:
            print(f"{Fore.RED}错误：没有该债券持仓{Style.RESET_ALL}")
            return

        # 初始化 amount 变量
        sell_amount = 0.0

        try:
            sell_amount = int(input(f"请输入卖出数量（当前持仓：{int(current_amount)}）：")) # 数量显示为整数
            if sell_amount <= 0 or sell_amount > current_amount:
                raise ValueError
            sell_amount = float(sell_amount) # 将卖出数量转换为浮点数
        except ValueError as e:
            print(f"{Fore.RED}错误：{e}{Style.RESET_ALL}")
            return

        # 计算收益
        total_income = bond.current_price * sell_amount
        profit_loss = (bond.current_price - avg_price) * sell_amount # 计算盈亏
        self.player["cash"] = float(self.player.get("cash", 0.0)) + total_income if isinstance(self.player.get("cash", 0.0), (int, float)) else total_income # 确保现金是浮点数

        # 更新持仓
        new_holding_amount = current_amount - sell_amount
        if new_holding_amount <= 0.0: # 使用<=0.0处理浮点误差
            del bonds[code]
        else:
            # 只更新数量，平均成本价不变
            holding_data["amount"] = new_holding_amount
            bonds[code] = holding_data # 更新剩余数量 (浮点)

        self.player["bonds"] = bonds

        print(f"{Fore.GREEN}成功卖出 {int(sell_amount)} 单位 {bond.name}，获得{total_income:.2f}元{Style.RESET_ALL}") # 数量显示为整数，格式化收益为2位小数
        print(f"{Fore.GREEN}本次交易盈亏：{profit_loss:.2f}元{Style.RESET_ALL}") # 格式化盈亏为2位小数

        # 新增操作记录
        bond.operation_history.append({
            "day": self.day,
            "action": "卖出",
            "amount": int(sell_amount), # 操作记录数量保存为整数
            "price": bond.current_price
        })
        self.record_trade("债券", code, "卖出", sell_amount, bond.current_price) # 交易记录数量保存为浮点数
        self.add_exp(int(profit_loss / 1000))  # 盈利每1000元增加1点经验
        self.save_game()

    def short_stock(self):
        """股票做空功能 (已整合到bulk_stock_trade)"""
        pass # 此函数现在是bulk_stock_trade的一部分，保留pass或删除

    def cover_short(self):
         """平仓做空仓位 (已整合到bulk_stock_trade)"""
         pass # 此函数现在是bulk_stock_trade的一部分，保留pass或删除

    def show_portfolio(self):
        """显示玩家投资组合（增加做空仓位显示）"""
        print(f"{Fore.CYAN}=== 我的持仓 ==={Style.RESET_ALL}")
        # 确保从player字典获取的值是数字类型，默认为0.0
        cash = float(self.player.get('cash', 0.0)) if isinstance(self.player.get('cash', 0.0), (int, float)) else 0.0
        debt = float(self.player.get('debt', 0.0)) if isinstance(self.player.get('debt', 0.0), (int, float)) else 0.0

        print(f"现金：{cash:.2f}元") # 格式化为2位小数
        print(f"债务：{debt:.2f}元") # 格式化为2位小数

        total_stock_value = 0.0 # 确保总价值为浮点数
        print("\n股票持仓：")
        # 添加平均成本列
        print("代码 | 名称 | 数量 | 平均成本(元) | 当前价(元) | 总价值(元) | 总盈亏(元)") # 添加盈亏列
        print("-" * 90) # 调整分隔线长度
        stocks = self.player.get('stocks', {})
        if isinstance(stocks, dict):
            # 确保items()返回字典视图
            for code, holding_data in stocks.items():
                stock = self.market.stock_dict.get(code)
                # 确保holding_data是字典且包含必要键，数量和平均价格是数字
                if stock and isinstance(holding_data, dict) and isinstance(holding_data.get("amount"), (int, float)) and isinstance(holding_data.get("avg_price"), (int, float)):
                    amount = float(holding_data["amount"])
                    avg_price = float(holding_data["avg_price"])
                    current_price = float(stock.current_price)
                    value = current_price * amount # 确保浮点数运算
                    total_stock_value += value
                    profit_loss = (current_price - avg_price) * amount # 计算总盈亏

                    # 根据盈亏确定颜色
                    color = Fore.GREEN if profit_loss > 0 else (Fore.RED if profit_loss < 0 else Style.RESET_ALL)

                    print(f"{code} | {stock.name} | {int(amount)} | {avg_price:.2f} | {current_price:.2f} | {value:.2f} | {color}{profit_loss:.2f}{Style.RESET_ALL}") # 格式化并显示所有信息，数量显示为整数，盈亏带颜色
                else:
                    print(f"错误：股票持仓 {code} 数据异常")

        # 检查stocks是否为空或非字典
        if not stocks or not isinstance(stocks, dict) or not stocks:
            print("(空)")

        total_bond_value = 0.0 # 确保总价值为浮点数
        print("\n债券持仓：")
        print("代码 | 名称 | 数量 | 平均成本(元) | 当前价(元) | 总价值(元) | 总盈亏(元)") # 添加盈亏列
        print("-" * 90) # 调整分隔线长度
        bonds = self.player.get('bonds', {})
        if isinstance(bonds, dict):
             # 确保items()返回字典视图
            for code, holding_data in bonds.items():
                bond = self.market.bond_dict.get(code)
                 # 确保holding_data是字典且包含必要键，数量和平均价格是数字
                if bond and isinstance(holding_data, dict) and isinstance(holding_data.get("amount"), (int, float)) and isinstance(holding_data.get("avg_price"), (int, float)):
                    amount = float(holding_data["amount"])
                    avg_price = float(holding_data["avg_price"])
                    current_price = float(bond.current_price)
                    value = current_price * amount # 确保浮点数运算
                    total_bond_value += value
                    profit_loss = (current_price - avg_price) * amount # 计算总盈亏

                    # 根据盈亏确定颜色
                    color = Fore.GREEN if profit_loss > 0 else (Fore.RED if profit_loss < 0 else Style.RESET_ALL)

                    print(f"{code} | {bond.name} | {int(amount)} | {avg_price:.2f} | {current_price:.2f} | {value:.2f} | {color}{profit_loss:.2f}{Style.RESET_ALL}") # 格式化并显示所有信息，数量显示为整数，盈亏带颜色
                else:
                    print(f"错误：债券持仓 {code} 数据异常")

         # 检查bonds是否为空或非字典
        if not bonds or not isinstance(bonds, dict) or not bonds:
            print("(空)")

        # 显示做空仓位
        print(f"\n{Fore.RED}=== 做空仓位 (理论盈亏) ==={Style.RESET_ALL}") # 标注为理论盈亏
        shorts = self.player.get("shorts", {})
        if not isinstance(shorts, dict) or not shorts:
            print("当前没有做空仓位")
        else:
            print("代码 | 名称 | 数量 | 借入价格(元) | 当前价格(元) | 理论盈亏(元)") # 添加盈亏列
            print("-" * 90) # 调整分隔线长度
             # 确保items()返回字典视图
            for code, data in shorts.items():
                stock = self.market.stock_dict.get(code)
                # 确保data是列表且包含足够元素，元素是数字
                if isinstance(data, list) and len(data) >= 2 and isinstance(data[0], (int, float)) and isinstance(data[1], (int, float)):
                    current_price = float(stock.current_price) if stock else 0.0
                    borrow_price = float(data[1])
                    amount = float(data[0])
                    # 做空盈亏 = (借入价格 - 当前价格) * 数量
                    profit = (borrow_price - current_price) * amount

                    # 根据盈亏确定颜色
                    color = Fore.GREEN if profit > 0 else (Fore.RED if profit < 0 else Style.RESET_ALL)

                    print(f"{code} | {stock.name if stock else '未知'} | {int(amount)} | {borrow_price:.2f} | {current_price:.2f} | {color}{profit:.2f}{Style.RESET_ALL}") # 格式化并显示所有信息，数量显示为整数，盈亏带颜色
                else:
                    print(f"错误：做空仓位 {code} 数据异常")

        # 计算总资产和净资产，确保所有组成部分都是浮点数
        total_assets = cash + total_stock_value + total_bond_value
        net_assets = total_assets - debt

        print(f"\n总资产：{total_assets:.2f}元") # 格式化总资产
        print(f"净资产：{net_assets:.2f}元") # 格式化净资产

    def show_asset_trend(self):
        """显示资产趋势 (使用总资产历史) """
        print(f"{Fore.CYAN}=== 资产趋势 ==={Style.RESET_ALL}")
        if not self.total_assets_history:
            print("暂无历史数据")
            return

        max_days = min(30, len(self.total_assets_history))
        history = self.total_assets_history[-max_days:]
        # 确保历史数据是数字
        history_numeric = [float(h) for h in history if isinstance(h, (int, float))]

        if not history_numeric:
             print("历史数据格式错误")
             return

        min_val = min(history_numeric)
        max_val = max(history_numeric)
        if max_val == min_val:
            max_val = min_val + 1.0 # Prevent division by zero if all values are the same, ensure float

        term_width = shutil.get_terminal_size().columns
        # Adjust chart width calculation for clarity and prevent excessive width
        chart_width = min(80, term_width - 25) # Leave space for day and value labels

        print(f"近 {max_days} 天总资产趋势 (单位：元)")
        print(f"范围：{min_val:.2f}元 ~ {max_val:.2f}元") # 格式化范围

        for i, val in enumerate(history_numeric): # 使用numeric历史数据
            # Calculate relative position within the chart range
            norm_val = (val - min_val) / (max_val - min_val)
            bar_len = int(norm_val * chart_width)

            # Determine color based on change from previous day
            color = Style.RESET_ALL
            if i > 0:
                # 确保前一天数据是数字
                prev_val = history_numeric[i-1]
                if val > prev_val:
                    color = Fore.GREEN
                elif val < prev_val:
                    color = Fore.RED

            # Format day and value labels
            day_num = self.day - len(history_numeric) + i + 1 # 使用numeric历史数据长度
            day_label = f"第{day_num:3d}天 |"
            # Format with comma separator, replace with underscore to avoid f-string issues
            value_label = f"{val:,.2f}元".replace(",", "_") .rjust(12) # 右对齐并格式化价值

            # Print the bar and labels
            # Use ljust to pad the line to terminal width for alignment, though perfect alignment is tricky with variable width chars
            print(f"{day_label} {color}{'█' * bar_len}{Style.RESET_ALL} {value_label}")
        # Add legend for clarity
        print(f"\n{Fore.YELLOW}图例说明：{Style.RESET_ALL}")
        print(f"{Fore.GREEN}███绿色：当日总资产上涨{Style.RESET_ALL}")
        print(f"{Fore.RED}███红色：当日总资产下跌{Style.RESET_ALL}")
        print("███白色：当日总资产无变化或首日")
        print("柱状长度反映相对总资产区间，非绝对涨跌幅")
        print("（注意：由于终端字符限制，图表精度有限）")

    def show_horizontal_chart(self):
        """优化后的水平走势图显示（完整修复版）"""
        print("\n=== 资产价格走势分析 ===")
        code = input("请输入资产代码：").upper()
        asset = (self.market.stock_dict.get(code) or
                self.market.bond_dict.get(code))

        if not asset or not asset.history:
            print("无效资产代码或没有历史数据")
            return

        # 动态终端适配
        term_width, _ = shutil.get_terminal_size()
        # Adjust max_bar_width calculation for clarity and prevent excessive width
        max_bar_width = max(30, term_width - 35)  # 为价格标签留出空间
        # Limit displayed days based on available history and chart width
        max_days_to_show = min(len(asset.history), max_bar_width) # Display at most chart_width days

        # 获取历史数据（最近 max_days_to_show 天）
        history_to_show = asset.history[-max_days_to_show:]
        day_count = len(history_to_show)
        start_day_display = self.day - day_count + 1

        # 计算显示参数
        # Extract prices from the history list of dicts, ensure they are numbers
        prices_to_show = [float(entry["price"]) for entry in history_to_show if isinstance(entry.get("price"), (int, float))]

        if not prices_to_show:
            print("历史价格数据格式错误")
            return

        min_price = min(prices_to_show) if prices_to_show else 0.0 # Ensure float default
        max_price = max(prices_to_show) if prices_to_show else (min_price + 1.0) # Prevent division by zero, ensure float
        price_range = max(max_price - min_price, 1.0)  # 防止除零，确保浮点数

        # 打印头部信息
        print(f"\n{asset.name} ({code}) 近期价格走势".center(term_width))
        print(f"当前第 {self.day} 天 | 显示最近 {day_count} 个交易日".center(term_width))
        print(f"历史价格范围：{min_price:.2f}元 ~ {max_price:.2f}元".center(term_width)) # 格式化范围

        # 绘制走势图
        for idx in range(day_count):
            current_entry = history_to_show[idx]
            # 确保当前价格是数字
            current_price = float(current_entry.get("price", 0.0)) if isinstance(current_entry.get("price"), (int, float)) else 0.0

            # Get previous day's price from history_to_show if available, ensure number
            prev_price = float(history_to_show[idx-1].get("price", 0.0)) if idx > 0 and isinstance(history_to_show[idx-1].get("price"), (int, float)) else current_price

            # Calculate relative position within the chart range
            # Avoid division by zero if price_range is 0
            norm_val = (current_price - min_price) / price_range if price_range > 0 else 0.0
            bar_width = max(1, int(norm_val * max_bar_width))  # 确保最小显示宽度

            # Determine color
            color = Style.RESET_ALL # Default color
            if idx > 0:
                if current_price > prev_price:
                    color = Fore.GREEN
                elif current_price < prev_price:
                    color = Fore.RED

            # Build bar and labels
            bar = f"{color}{'█' * bar_width}"
            # Format price label with fixed width
            # Format price label with fixed width and comma separators
            price_label = f"{Style.RESET_ALL}{current_price:,.2f}元".replace(",", "_").rjust(12) # Right justify price label
            day_label = f" (第{start_day_display + idx}天)" if idx % 5 == 0 or idx == day_count-1 else ""

            # Print the line, padding to terminal width
            line = f"{bar}{price_label}{day_label}"
            print(line.ljust(term_width))

        # 图例说明
        print(f"\n{Fore.YELLOW}图例说明：{Style.RESET_ALL}")
        print(f"{Fore.GREEN}███绿色：当日价格上涨{Style.RESET_ALL}")
        print(f"{Fore.RED}███红色：当日价格下跌{Style.RESET_ALL}")
        print("███白色：当日价格无变化或首日")
        print("柱状长度反映相对价格区间，非绝对涨跌幅")
        print("（注意：由于终端字符限制，图表精度有限）")

    def bulk_stock_trade(self):
        """整合股票交易和做空功能"""
        self.show_stock_market()
        code = input("输入股票代码：").upper()

        # 验证股票代码有效性
        if code not in self.market.stock_dict:
            print(f"{Fore.RED}错误：无效的股票代码{Style.RESET_ALL}")
            return

        stock = self.market.stock_dict[code]
        action = input("请选择操作 (1.买入 / 2.卖出 / 3.做空 / 4.平仓做空): ")

        # 定义amount变量并初始化，确保在try块外已定义并为数字类型
        amount = 0.0

        # 获取并验证交易数量 (买入、卖出、做空需要数量输入)
        if action in ["1", "2", "3"]:
            try:
                amount = int(input(f"操作数量（当前价：{stock.current_price:.2f}元/股）："))
                if amount <= 0:
                    raise ValueError("数量必须为正整数")
                amount = float(amount)
                # 验证土豪模式
                if action in ["1", "3"] and not self.validate_tycoon_purchase(amount):
                    return
            except ValueError as e:
                print(f"{Fore.RED}错误：{e}{Style.RESET_ALL}")
                return

        # 买入逻辑
        if action == "1":
            total_cost = stock.current_price * amount
            current_cash = float(self.player.get("cash", 0.0)) if isinstance(self.player.get("cash", 0), (int, float)) else 0.0 # 确保现金是浮点数
            if total_cost > current_cash:
                print(f"{Fore.RED}错误：资金不足，需要{total_cost:.2f}元{Style.RESET_ALL}") # 使用.2f格式化金额
            else:
                self.player["cash"] = current_cash - total_cost
                stocks = self.player.get("stocks", {})
                if isinstance(stocks, dict):
                    current_holding = float(stocks.get(code, 0.0)) if isinstance(stocks.get(code), dict) and isinstance(stocks.get(code).get("amount"), (int, float)) else 0.0 # 确保持仓是浮点数并检查结构
                    stocks[code] = {"amount": current_holding + amount, "avg_price": float(stocks.get(code, {}).get("avg_price", stock.current_price))}
                    self.player["stocks"] = stocks
                print(f"{Fore.GREEN}成功买入 {int(amount)} 股 {stock.name}{Style.RESET_ALL}") # 数量显示为整数
                # 新增操作记录
                stock.operation_history.append({
                    "day": self.day,
                    "action": "买入",
                    "amount": int(amount), # 操作记录数量保存为整数
                    "price": stock.current_price
                })
                self.record_trade("股票", code, "买入", amount, stock.current_price) # 交易记录数量保存为浮点数
                self.add_exp(20)  # 购买股票增加20点经验
                self.save_game()
                        
        # 卖出逻辑
        elif action == "2":
            stocks = self.player.get("stocks", {})
            # 确保持仓是字典且包含该股票代码，然后获取amount，否则为0.0
            current_holding = float(stocks.get(code, {}).get("amount", 0.0)) if isinstance(stocks, dict) and isinstance(stocks.get(code), dict) and isinstance(stocks.get(code).get("amount"), (int, float)) else 0.0 # 确保持仓是浮点数并检查结构

            # 强化类型检查和数量检查
            if current_holding < amount:
                print(f"{Fore.RED}错误：持仓不足，当前持有 {int(current_holding)} 股{Style.RESET_ALL}") # 数量显示为整数
                return

            # 计算收益和盈亏
            total_income = stock.current_price * amount
            # 获取平均成本价，确保是数字
            avg_price = float(stocks[code].get("avg_price", 0.0)) if isinstance(stocks.get(code), dict) and "avg_price" in stocks.get(code) else 0.0
            profit_loss = (stock.current_price - avg_price) * amount # 计算盈亏

            self.player["cash"] = float(self.player.get("cash", 0.0)) + total_income if isinstance(self.player.get("cash", 0.0), (int, float)) else total_income # 确保现金是浮点数

            # 更新持仓数量，平均成本价不变
            if isinstance(stocks, dict):
                # 确保获取持仓数据时处理可能的数据异常
                holding_data = stocks.get(code)
                if isinstance(holding_data, dict) and "amount" in holding_data:
                    new_holding_amount = float(holding_data["amount"]) - amount
                    if new_holding_amount <= 0.0: # 使用<=0.0处理浮点误差
                        if code in stocks:
                            del stocks[code]  # 完全卖出后移除持仓记录
                    else:
                         holding_data["amount"] = new_holding_amount # 更新剩余数量 (浮点)
                         stocks[code] = holding_data # 更新持仓字典
                else:
                    print(f"{Fore.RED}内部错误：卖出时获取持仓数据异常 for {code}{Style.RESET_ALL}")
                    return # 数据异常则退出

                self.player["stocks"] = stocks

            print(f"{Fore.GREEN}成功卖出 {int(amount)} 股 {stock.name}，获得{total_income:.2f}元{Style.RESET_ALL}") # 数量显示为整数，格式化收益
            print(f"{Fore.GREEN}本次交易盈亏：{profit_loss:.2f}元{Style.RESET_ALL}") # 格式化盈亏

            # 新增操作记录
            stock.operation_history.append({
                "day": self.day,
                "action": "卖出",
                "amount": int(amount), # 操作记录数量保存为整数
                "price": stock.current_price
            })
            self.record_trade("股票", code, "卖出", amount, stock.current_price) # 交易记录数量保存为浮点数
            self.add_exp(int(profit_loss / 1000))  # 盈利每1000元增加1点经验
            self.save_game()

        # 做空逻辑
        elif action == "3":
             # amount变量已经在try块外初始化并获取
             # 计算保证金（假设50%保证金率），确保浮点数运算
             margin_required = stock.current_price * amount * 0.5
             current_cash = float(self.player.get("cash", 0.0)) if isinstance(self.player.get("cash", 0), (int, float)) else 0.0 # 确保现金是浮点数
             if current_cash < margin_required:
                 print(f"{Fore.RED}错误：保证金不足，需要{margin_required:.2f}元{Style.RESET_ALL}") # 格式化保证金
                 return

             # 记录做空仓位，确保借入价格是浮点数，数量是浮点数以便计算
             # 做空仓位存储 {代码: [数量(float), 借入价格(float), 借入天数(int)]}
             shorts = self.player.get("shorts", {})
             if not isinstance(shorts, dict): # 确保shorts是字典
                  shorts = {}

             # 如果已经有做空仓位，更新数量和借入价格（使用加权平均）
             if code in shorts and isinstance(shorts[code], list) and len(shorts[code]) >= 3:
                 existing_amount = float(shorts[code][0])
                 existing_borrow_price = float(shorts[code][1])
                 new_total_amount = existing_amount + amount
                 new_borrow_price = ((existing_borrow_price * existing_amount) + (stock.current_price * amount)) / new_total_amount if new_total_amount > 0 else 0.0
                 shorts[code] = [new_total_amount, new_borrow_price, self.day] # 更新借入天数为最新的
             else:
                 # 新建做空仓位记录
                 shorts[code] = [float(amount), float(stock.current_price), self.day]

             self.player["cash"] = current_cash + stock.current_price * amount - margin_required
             self.player["shorts"] = shorts

             print(f"{Fore.GREEN}成功做空 {int(amount)} 股 {stock.name}，保证金已扣除{margin_required:.2f}元{Style.RESET_ALL}") # 数量显示为整数，格式化保证金
             # 新增操作记录
             stock.operation_history.append({
                 "day": self.day,
                 "action": "做空",
                 "amount": int(amount), # 操作记录数量保存为整数
                 "price": stock.current_price
             })
             self.record_trade("股票", code, "做空", amount, stock.current_price) # 交易记录数量保存为浮点数
             self.add_exp(30)  # 做空增加30点经验
             self.save_game()

        # 平仓做空逻辑
        elif action == "4":
             # 平仓数量单独获取，确保为数字类型
             amount_to_cover = 0.0
             try:
                 shorts = self.player.get("shorts", {})
                 if not isinstance(shorts, dict) or code not in shorts or not isinstance(shorts[code], list) or len(shorts[code]) < 3:
                     print(f"{Fore.RED}错误：没有该股票的做空仓位或数据异常{Style.RESET_ALL}")
                     return
                 # 确保获取当前做空数量时处理可能的数据异常
                 current_short_amount = float(shorts[code][0]) if isinstance(shorts[code][0], (int, float)) else 0.0

                 amount_to_cover = int(input(f"平仓数量（当前做空：{int(current_short_amount)}股）：")) # 数量显示为整数
                 if amount_to_cover <= 0 or amount_to_cover > current_short_amount:
                      print(f"{Fore.RED}错误：无效或超过做空数量{Style.RESET_ALL}")
                      return
                 amount_to_cover = float(amount_to_cover) # 将平仓数量转换为浮点数
             except ValueError as e:
                 print(f"{Fore.RED}错误：{e}{Style.RESET_ALL}")
                 return

             # shorts变量已经在try块外获取并验证
             short_data = shorts[code]
             borrow_price = float(short_data[1]) # 确保借入价格是浮点数
             original_short_amount = float(short_data[0]) # 确保原始做空数量是浮点数

             # 计算买回成本，确保浮点数运算
             buyback_cost = stock.current_price * amount_to_cover
             current_cash = float(self.player.get("cash", 0.0)) if isinstance(self.player.get("cash", 0), (int, float)) else 0.0 # 确保现金是浮点数
             if current_cash < buyback_cost:
                 print(f"{Fore.RED}错误：现金不足，需要{buyback_cost:.2f}元{Style.RESET_ALL}") # 格式化成本
                 return

             # 计算盈亏 (只计算平仓部分的盈亏)，确保浮点数运算
             profit_per_share = borrow_price - stock.current_price
             total_profit = profit_per_share * amount_to_cover

             # 返还平仓部分的保证金，并结算盈亏
             # 保证金计算基于借入价格，返还时应按比例
             returned_margin = (amount_to_cover / original_short_amount) * (borrow_price * original_short_amount * 0.5) if original_short_amount > 0 else 0.0 # 避免除以零
             self.player["cash"] = current_cash + total_profit + returned_margin # 确保现金是浮点数

             # 更新做空仓位
             short_data[0] = original_short_amount - amount_to_cover
             if short_data[0] <= 0.0: # 使用<=0.0处理浮点误差
                 del shorts[code]
             else:
                 shorts[code] = short_data # 更新剩余数量 (浮点)

             self.player["shorts"] = shorts
             print(f"{Fore.GREEN}平仓 {int(amount_to_cover)} 股成功，净盈亏：{total_profit:.2f}元{Style.RESET_ALL}") # 数量显示为整数，格式化盈亏
             # 新增操作记录
             stock.operation_history.append({
                 "day": self.day,
                 "action": "平仓",
                 "amount": int(amount_to_cover), # 操作记录数量保存为整数
                 "price": stock.current_price
             })
             self.record_trade("股票", code, "平仓做空", amount_to_cover, stock.current_price) # 交易记录数量保存为浮点数
             self.add_exp(int(total_profit / 1000))  # 盈利每1000元增加1点经验
             self.save_game()

        else:
            print(f"{Fore.RED}错误：无效的操作选择{Style.RESET_ALL}")
            # 不需要保存游戏，因为没有成功交易
            return

        # self.save_game() # 成功交易后在各个分支内部保存游戏

    def daily_update(self):
        """增强的每日结算"""
        self.day += 1
        self.market.set_day(self.day)
        # 使用游戏天数获取季节
        season = self.season.current_season(self.day)

        # 更新股票和债券价格及历史
        self.market.update_stocks(season["stock_vol"], self.day)
        self.market.update_bonds(season, self.day)

        # 每日资产快照
        total_assets = self.calculate_total_assets()
        self.total_assets_history.append(total_assets)
        if len(self.total_assets_history) > 365: # 保留一年数据
            self.total_assets_history.pop(0)

        # TODO: 每日债务利息计算
        # TODO: 每日做空利息计算
        self.save_game()

    def show_trade_history(self):
        """显示交易历史"""
        print(f"\n{Fore.CYAN}=== 交易历史 ==={Style.RESET_ALL}")
        if not self.trade_history:
            print("暂无交易历史")
            return
        # 价格显示单位修正为元，格式化
        print("日期 | 类型 | 代码 | 操作 | 数量 | 价格(元)")
        print("-" * 60)
        # 显示最近30条，并格式化价格为元
        for record in self.trade_history[-30:]:
            # 确保价格是数字
            price = float(record.get("price", 0.0)) if isinstance(record.get("price"), (int, float)) else 0.0
            print(f"{record.get('day','未知')}日 | {record.get('type','未知')} | {record.get('code','未知')} | "
                  f"{record.get('action','未知')} | {record.get('amount','未知')} | {price:.2f}") # 格式化价格为2位小数

    def show_asset_history(self):
        """显示资产详细历史"""
        print("\n=== 资产历史分析 ===")
        code = input("请输入资产代码：").upper()
        asset = (self.market.stock_dict.get(code) or
                self.market.bond_dict.get(code))

        if not asset:
            print("无效资产代码")
            return

        # 显示价格历史
        print(f"\n{Fore.YELLOW}{asset.name} ({code}) 价格历史：{Style.RESET_ALL}")
        if not asset.history:
             print("暂无价格历史数据")
        else:
            # 价格显示单位修正为元，格式化
            print("日期 | 价格(元)")
            print("-" * 20)
            # 显示最近30天价格历史，并格式化价格为元
            for h in asset.history[-30:]:
                # 确保历史数据是字典且价格是数字
                if isinstance(h, dict) and isinstance(h.get("day"), int) and isinstance(h.get("price"), (int, float)):
                    day = h["day"]
                    price = float(h["price"])
                    print(f"{day}日 | {price:.2f}") # 格式化价格为2位小数
                else:
                    print(f"历史数据格式错误: {h}")

        # 显示操作历史
        print(f"\n{Fore.YELLOW}{asset.name} ({code}) 操作历史：{Style.RESET_ALL}")
        if not asset.operation_history:
            print("暂无操作历史数据")
        else:
             # 价格显示单位修正为元，格式化
            print("日期 | 操作 | 数量 | 价格(元)")
            print("-" * 40)
            # 显示最近30条操作历史，并格式化价格为元
            for op in asset.operation_history[-30:]: # 显示最近30条
                 # 确保操作数据是字典且包含必要键，数量和价格是数字
                 if isinstance(op, dict) and isinstance(op.get("day"), int) and isinstance(op.get("amount"), (int, float)) and isinstance(op.get("price"), (int, float)):
                    day = op["day"]
                    amount = op["amount"]
                    price = float(op["price"])
                    action = op.get("action", "未知")
                    # 根据操作类型调整显示
                    action_desc = f"{action} {amount}股" if asset in self.market.stock_dict.values() else f"{action} {amount}单位"
                    print(f"{day}日 | {action_desc} | {amount} | {price:.2f}") # 格式化价格为2位小数
                 else:
                    print(f"操作历史数据格式错误: {op}")


    def record_trade(self, type, code, action, amount, price):
        """记录交易历史"""
        # 确保记录的数据类型正确
        record = {
            "day": int(self.day),
            "type": str(type),
            "code": str(code),
            "action": str(action),
            "amount": float(amount), # 数量保存为浮点数以便后续计算
            "price": float(price) # 价格保存为浮点数
        }
        self.trade_history.append(record)

    def screen_good_investments(self):
        """自动筛选近指定天数内势头很猛的股票和债券"""
        print(f"{Fore.CYAN}=== 自动筛选好投资 ==={Style.RESET_ALL}")
        try:
            days = int(input("请输入筛选天数："))
            if days <= 0:
                print("天数必须大于0")
                return
        except ValueError:
            print("无效输入，天数必须是整数")
            return
        
        # 筛选股票
        print(f"\n{Fore.YELLOW}股票筛选结果（近{days}天涨幅）：{Style.RESET_ALL}")
        stock_results = []
        for stock in self.market.stocks:
            if len(stock.history) >= days:
                recent_history = stock.history[-days:]
                start_price = float(recent_history[0].get("price", 0.0))
                end_price = float(recent_history[-1].get("price", 0.0))
                if start_price > 0:
                    percentage_change = (end_price - start_price) / start_price * 100
                    stock_results.append((stock, percentage_change))
        
        # 按涨幅排序并显示前3名
        stock_results.sort(key=lambda x: x[1], reverse=True)
        for idx, (stock, change) in enumerate(stock_results[:3], 1):
            color = Fore.GREEN if change > 0 else (Fore.RED if change < 0 else Style.RESET_ALL)
            print(f"{idx}. {stock.code} - {stock.name}: {color}{change:.2f}%{Style.RESET_ALL}")
        if not stock_results:
            print("暂无足够历史数据的股票")
        
        # 筛选债券
        print(f"\n{Fore.YELLOW}债券筛选结果（近{days}天涨幅）：{Style.RESET_ALL}")
        bond_results = []
        for bond in self.market.bonds:
            if len(bond.history) >= days:
                recent_history = bond.history[-days:]
                start_price = float(recent_history[0].get("price", 0.0))
                end_price = float(recent_history[-1].get("price", 0.0))
                if start_price > 0:
                    percentage_change = (end_price - start_price) / start_price * 100
                    bond_results.append((bond, percentage_change))
        
        # 按涨幅排序并显示前2名
        bond_results.sort(key=lambda x: x[1], reverse=True)
        for idx, (bond, change) in enumerate(bond_results[:2], 1):
            color = Fore.GREEN if change > 0 else (Fore.RED if change < 0 else Style.RESET_ALL)
            print(f"{idx}. {bond.code} - {bond.name}: {color}{change:.2f}%{Style.RESET_ALL}")
        if not bond_results:
            print("暂无足够历史数据的债券")
        
        # 询问用户是否查看详情
        choice = input("\n是否查看具体详情？(y/n)：").lower()
        if choice == 'y':
            code = input("请输入资产代码：").upper()
            asset = self.market.stock_dict.get(code) or self.market.bond_dict.get(code)
            if asset:
                # 显示价格走势
                print(f"\n{Fore.YELLOW}{asset.name} ({code}) 价格走势：{Style.RESET_ALL}")
                self.show_horizontal_chart_for_asset(asset)
                # 询问是否购买
                buy_choice = input("是否购买该资产？(y/n)：").lower()
                if buy_choice == 'y':
                    if asset in self.market.stocks:
                        self.bulk_stock_trade_for_asset(asset)
                    elif asset in self.market.bonds:
                        self.buy_bonds_for_asset(asset)
            else:
                print("无效的资产代码")

    def show_horizontal_chart_for_asset(self, asset):
        """为特定资产显示水平走势图"""
        print(f"\n=== {asset.name} 价格走势分析 ===")
        if not asset.history:
            print("没有历史数据")
            return

        # 动态终端适配
        term_width, _ = shutil.get_terminal_size()
        max_bar_width = max(30, term_width - 35)  # 为价格标签留出空间
        max_days_to_show = min(len(asset.history), max_bar_width)

        # 获取历史数据
        history_to_show = asset.history[-max_days_to_show:]
        day_count = len(history_to_show)
        start_day_display = self.day - day_count + 1

        # 计算显示参数
        prices_to_show = [float(entry["price"]) for entry in history_to_show if isinstance(entry.get("price"), (int, float))]
        if not prices_to_show:
            print("历史价格数据格式错误")
            return

        min_price = min(prices_to_show) if prices_to_show else 0.0
        max_price = max(prices_to_show) if prices_to_show else (min_price + 1.0)
        price_range = max(max_price - min_price, 1.0)

        # 打印头部信息
        print(f"\n{asset.name} ({asset.code}) 近期价格走势".center(term_width))
        print(f"当前第 {self.day} 天 | 显示最近 {day_count} 个交易日".center(term_width))
        print(f"历史价格范围：{min_price:.2f}元 ~ {max_price:.2f}元".center(term_width))

        # 绘制走势图
        for idx in range(day_count):
            current_entry = history_to_show[idx]
            current_price = float(current_entry.get("price", 0.0)) if isinstance(current_entry.get("price"), (int, float)) else 0.0
            prev_price = float(history_to_show[idx-1].get("price", 0.0)) if idx > 0 and isinstance(history_to_show[idx-1].get("price"), (int, float)) else current_price

            norm_val = (current_price - min_price) / price_range if price_range > 0 else 0.0
            bar_width = max(1, int(norm_val * max_bar_width))

            color = Style.RESET_ALL
            if idx > 0:
                if current_price > prev_price:
                    color = Fore.GREEN
                elif current_price < prev_price:
                    color = Fore.RED

            bar = f"{color}{'█' * bar_width}"
            price_label = f"{Style.RESET_ALL}{current_price:,.2f}元".replace(",", "_").rjust(12)
            day_label = f" (第{start_day_display + idx}天)" if idx % 5 == 0 or idx == day_count-1 else ""

            line = f"{bar}{price_label}{day_label}"
            print(line.ljust(term_width))

        # 图例说明
        print(f"\n{Fore.YELLOW}图例说明：{Style.RESET_ALL}")
        print(f"{Fore.GREEN}███绿色：当日价格上涨{Style.RESET_ALL}")
        print(f"{Fore.RED}███红色：当日价格下跌{Style.RESET_ALL}")
        print("███白色：当日价格无变化或首日")
        print("柱状长度反映相对价格区间，非绝对涨跌幅")
        print("（注意：由于终端字符限制，图表精度有限）")

    def bulk_stock_trade_for_asset(self, stock):
        """为特定股票执行交易"""
        print(f"\n{Fore.CYAN}=== 股票交易 - {stock.name} ==={Style.RESET_ALL}")
        action = input("请选择操作 (1.买入 / 2.卖出 / 3.做空 / 4.平仓做空): ")

        amount = 0.0
        if action in ["1", "2", "3"]:
            try:
                amount = int(input(f"操作数量（当前价：{stock.current_price:.2f}元/股）："))
                if amount <= 0:
                    raise ValueError("数量必须为正整数")
                amount = float(amount)
            except ValueError as e:
                print(f"{Fore.RED}错误：{e}{Style.RESET_ALL}")
                return

        if action == "1":
            total_cost = stock.current_price * amount
            current_cash = float(self.player.get("cash", 0.0)) if isinstance(self.player.get("cash", 0), (int, float)) else 0.0
            if total_cost > current_cash:
                print(f"{Fore.RED}错误：资金不足，需要{total_cost:.2f}元{Style.RESET_ALL}")
            else:
                self.player["cash"] = current_cash - total_cost
                stocks = self.player.get("stocks", {})
                if isinstance(stocks, dict):
                    current_holding = float(stocks.get(stock.code, {}).get("amount", 0.0)) if isinstance(stocks.get(stock.code), dict) else 0.0
                    stocks[stock.code] = {"amount": current_holding + amount, "avg_price": float(stocks.get(stock.code, {}).get("avg_price", stock.current_price))}
                    self.player["stocks"] = stocks
                print(f"{Fore.GREEN}成功买入 {int(amount)} 股 {stock.name}{Style.RESET_ALL}")
                stock.operation_history.append({
                    "day": self.day,
                    "action": "买入",
                    "amount": int(amount),
                    "price": stock.current_price
                })
                self.record_trade("股票", stock.code, "买入", amount, stock.current_price)
                self.save_game()
        elif action == "2":
            stocks = self.player.get("stocks", {})
            current_holding = float(stocks.get(stock.code, {}).get("amount", 0.0)) if isinstance(stocks, dict) else 0.0
            if current_holding < amount:
                print(f"{Fore.RED}错误：持仓不足，当前持有 {int(current_holding)} 股{Style.RESET_ALL}")
                return

            total_income = stock.current_price * amount
            avg_price = float(stocks[stock.code].get("avg_price", 0.0)) if isinstance(stocks.get(stock.code), dict) and "avg_price" in stocks.get(stock.code) else 0.0
            profit_loss = (stock.current_price - avg_price) * amount

            self.player["cash"] = float(self.player.get("cash", 0.0)) + total_income if isinstance(self.player.get("cash", 0.0), (int, float)) else total_income

            if isinstance(stocks, dict):
                holding_data = stocks.get(stock.code)
                if isinstance(holding_data, dict) and "amount" in holding_data:
                    new_holding_amount = float(holding_data["amount"]) - amount
                    if new_holding_amount <= 0.0:
                        if stock.code in stocks:
                            del stocks[stock.code]
                    else:
                        holding_data["amount"] = new_holding_amount
                        stocks[stock.code] = holding_data
                else:
                    print(f"{Fore.RED}内部错误：卖出时获取持仓数据异常 for {stock.code}{Style.RESET_ALL}")
                    return
                self.player["stocks"] = stocks

            print(f"{Fore.GREEN}成功卖出 {int(amount)} 股 {stock.name}，获得{total_income:.2f}元{Style.RESET_ALL}")
            print(f"{Fore.GREEN}本次交易盈亏：{profit_loss:.2f}元{Style.RESET_ALL}")

            if profit_loss > 0:
                self.add_exp(int(profit_loss / 1000))  # 盈利每1000元增加1点经验

            stock.operation_history.append({
                "day": self.day,
                "action": "卖出",
                "amount": int(amount),
                "price": stock.current_price
            })
            self.record_trade("股票", stock.code, "卖出", amount, stock.current_price)
            self.save_game()
        elif action == "3":
            margin_required = stock.current_price * amount * 0.5
            current_cash = float(self.player.get("cash", 0.0)) if isinstance(self.player.get("cash", 0), (int, float)) else 0.0
            if current_cash < margin_required:
                print(f"{Fore.RED}错误：保证金不足，需要{margin_required:.2f}元{Style.RESET_ALL}")
                return

            shorts = self.player.get("shorts", {})
            if not isinstance(shorts, dict):
                shorts = {}

            if stock.code in shorts and isinstance(shorts[stock.code], list) and len(shorts[stock.code]) >= 3:
                existing_amount = float(shorts[stock.code][0])
                existing_borrow_price = float(shorts[stock.code][1])
                new_total_amount = existing_amount + amount
                new_borrow_price = ((existing_borrow_price * existing_amount) + (stock.current_price * amount)) / new_total_amount if new_total_amount > 0 else 0.0
                shorts[stock.code] = [new_total_amount, new_borrow_price, self.day]
            else:
                shorts[stock.code] = [float(amount), float(stock.current_price), self.day]

            self.player["cash"] = current_cash + stock.current_price * amount - margin_required
            self.player["shorts"] = shorts

            print(f"{Fore.GREEN}成功做空 {int(amount)} 股 {stock.name}，保证金已扣除{margin_required:.2f}元{Style.RESET_ALL}")
            stock.operation_history.append({
                "day": self.day,
                "action": "做空",
                "amount": int(amount),
                "price": stock.current_price
            })
            self.record_trade("股票", stock.code, "做空", amount, stock.current_price)
            self.save_game()
        elif action == "4":
            amount_to_cover = 0.0
            try:
                shorts = self.player.get("shorts", {})
                if not isinstance(shorts, dict) or stock.code not in shorts or not isinstance(shorts[stock.code], list) or len(shorts[stock.code]) < 3:
                    print(f"{Fore.RED}错误：没有该股票的做空仓位或数据异常{Style.RESET_ALL}")
                    return
                current_short_amount = float(shorts[stock.code][0]) if isinstance(shorts[stock.code][0], (int, float)) else 0.0

                amount_to_cover = int(input(f"平仓数量（当前做空：{int(current_short_amount)}股）："))
                if amount_to_cover <= 0 or amount_to_cover > current_short_amount:
                    print(f"{Fore.RED}错误：无效或超过做空数量{Style.RESET_ALL}")
                    return
                amount_to_cover = float(amount_to_cover)
            except ValueError as e:
                print(f"{Fore.RED}错误：{e}{Style.RESET_ALL}")
                return

            short_data = shorts[stock.code]
            borrow_price = float(short_data[1])
            original_short_amount = float(short_data[0])

            buyback_cost = stock.current_price * amount_to_cover
            current_cash = float(self.player.get("cash", 0.0)) if isinstance(self.player.get("cash", 0), (int, float)) else 0.0
            if current_cash < buyback_cost:
                print(f"{Fore.RED}错误：现金不足，需要{buyback_cost:.2f}元{Style.RESET_ALL}")
                return

            profit_per_share = borrow_price - stock.current_price
            total_profit = profit_per_share * amount_to_cover

            returned_margin = (amount_to_cover / original_short_amount) * (borrow_price * original_short_amount * 0.5) if original_short_amount > 0 else 0.0
            self.player["cash"] = current_cash + total_profit + returned_margin

            short_data[0] = original_short_amount - amount_to_cover
            if short_data[0] <= 0.0:
                del shorts[stock.code]
            else:
                shorts[stock.code] = short_data

            self.player["shorts"] = shorts
            print(f"{Fore.GREEN}平仓 {int(amount_to_cover)} 股成功，净盈亏：{total_profit:.2f}元{Style.RESET_ALL}")
            stock.operation_history.append({
                "day": self.day,
                "action": "平仓",
                "amount": int(amount_to_cover),
                "price": stock.current_price
            })
            self.record_trade("股票", stock.code, "平仓做空", amount_to_cover, stock.current_price)
            self.save_game()
        else:
            print(f"{Fore.RED}错误：无效的操作选择{Style.RESET_ALL}")
            return

    def buy_bonds_for_asset(self, bond):
        """为特定债券执行购买"""
        print(f"\n{Fore.CYAN}=== 债券购买 - {bond.name} ==={Style.RESET_ALL}")
        try:
            amount = int(input("请输入购买数量："))
            if amount <= 0:
                raise ValueError("数量必须大于0")
            amount = float(amount)
        except ValueError:
            print("无效的数量")
            return

        total_cost = bond.current_price * amount
        current_cash = float(self.player.get('cash', 0.0)) if isinstance(self.player.get('cash', 0), (int, float)) else 0.0
        if total_cost > current_cash:
            print("资金不足")
            return

        self.player['cash'] = current_cash - total_cost
        bonds = self.player.get('bonds', {})
        if not isinstance(bonds, dict):
            bonds = {}

        if bond.code in bonds:
            existing_amount = float(bonds[bond.code].get("amount", 0.0))
            existing_avg_price = float(bonds[bond.code].get("avg_price", 0.0))
            new_total_amount = existing_amount + amount
            new_avg_price = ((existing_avg_price * existing_amount) + (bond.current_price * amount)) / new_total_amount if new_total_amount > 0 else 0.0
            bonds[bond.code] = {"amount": new_total_amount, "avg_price": new_avg_price}
        else:
            bonds[bond.code] = {"amount": amount, "avg_price": bond.current_price}

        self.player['bonds'] = bonds

        print(f"成功购买 {int(amount)} 单位 {bond.name}")
        bond.operation_history.append({
            "day": self.day,
            "action": "买入",
            "amount": int(amount),
            "price": bond.current_price
        })
        self.record_trade("债券", bond.code, "买入", amount, bond.current_price)
        self.save_game()

    def add_exp(self, amount):
        """增加经验并检查是否升级"""
        self.player["exp"] = int(self.player.get("exp", 0)) + amount if isinstance(self.player.get("exp"), (int, float)) else amount
        print(f"获得 {amount} 点经验！当前经验：{self.player['exp']}/{self.player['exp_to_next_level']}")
        if int(self.player.get("exp", 0)) >= int(self.player.get("exp_to_next_level", 100)):
            self.player["level"] = int(self.player.get("level", 1)) + 1
            self.player["exp"] = 0
            self.player["exp_to_next_level"] = int(int(self.player.get("exp_to_next_level", 100)) * 1.5)
            print(f"{Fore.GREEN}升级！当前等级：{self.player['level']}{Style.RESET_ALL}")
            if int(self.player.get("level", 1)) >= 10 and not self.tycoon_mode:
                print(f"{Fore.YELLOW}恭喜！已解锁土豪模式！{Style.RESET_ALL}")

# ========== 主菜单 ==========
def main_menu(game):
    while True:
        print("")
        print(f"{Fore.CYAN}=== 主菜单 ==={Style.RESET_ALL}")
        print(f"等级：{game.player['level']} | 经验：{game.player['exp']}/{game.player['exp_to_next_level']}")
        cash_display = float(game.player.get('cash', 0.0))
        debt_display = float(game.player.get('debt', 0.0))
        # 计算股票和债券的总价值，并显示详细拆分
        stocks_total_value = 0.0
        stocks_profit_loss = 0.0
        stocks_dict = game.player.get('stocks', {})
        stocks_breakdown = []
        if isinstance(stocks_dict, dict):
            for code, holding_data in stocks_dict.items():
                if isinstance(holding_data, dict) and isinstance(holding_data.get("amount"), (int, float)):
                    stock = game.market.stock_dict.get(code)
                    if stock:
                        value = float(stock.current_price) * float(holding_data["amount"])
                        profit_loss = (float(stock.current_price) - float(holding_data.get("avg_price", 0.0))) * float(holding_data["amount"])
                        stocks_total_value += value
                        stocks_profit_loss += profit_loss
                        stocks_breakdown.append(f"{value:.2f}")
        bonds_total_value = 0.0
        bonds_profit_loss = 0.0
        bonds_dict = game.player.get('bonds', {})
        bonds_breakdown = []
        if isinstance(bonds_dict, dict):
            for code, holding_data in bonds_dict.items():
                if isinstance(holding_data, dict) and isinstance(holding_data.get("amount"), (int, float)):
                    bond = game.market.bond_dict.get(code)
                    if bond:
                        value = float(bond.current_price) * float(holding_data["amount"])
                        profit_loss = (float(bond.current_price) - float(holding_data.get("avg_price", 0.0))) * float(holding_data["amount"])
                        bonds_total_value += value
                        bonds_profit_loss += profit_loss
                        bonds_breakdown.append(f"{value:.2f}")
        stocks_bonds_total_value = stocks_total_value + bonds_total_value
        stocks_breakdown_str = '+'.join(stocks_breakdown) if stocks_breakdown else '0.00'
        bonds_breakdown_str = '+'.join(bonds_breakdown) if bonds_breakdown else '0.00'
        print(f"股票总价值：{stocks_breakdown_str}={stocks_total_value:.2f}元")
        stocks_color = Fore.GREEN if stocks_profit_loss > 0 else (Fore.RED if stocks_profit_loss < 0 else Style.RESET_ALL)
        print(f"股票盈亏：{stocks_color}{stocks_profit_loss:.2f}元{Style.RESET_ALL}")
        print(f"债券总价值：{bonds_breakdown_str}={bonds_total_value:.2f}元")
        bonds_color = Fore.GREEN if bonds_profit_loss > 0 else (Fore.RED if bonds_profit_loss < 0 else Style.RESET_ALL)
        print(f"债券盈亏：{bonds_color}{bonds_profit_loss:.2f}元{Style.RESET_ALL}")
        total_profit_loss = stocks_profit_loss + bonds_profit_loss
        total_color = Fore.GREEN if total_profit_loss > 0 else (Fore.RED if total_profit_loss < 0 else Style.RESET_ALL)
        print(f"总盈亏：{total_color}{total_profit_loss:.2f}元{Style.RESET_ALL}")
        print(f"股票+债券总价值：{stocks_total_value:.2f}+{bonds_total_value:.2f}={stocks_bonds_total_value:.2f}元", end="")
        # 计算与昨天的盈亏对比
        if game.stocks_bonds_value_history and len(game.stocks_bonds_value_history) > 1:
            yesterday_value = float(game.stocks_bonds_value_history[-2]) if len(game.stocks_bonds_value_history) >= 2 and isinstance(game.stocks_bonds_value_history[-2], (int, float)) else 0.0
            today_value = float(game.stocks_bonds_value_history[-1]) if game.stocks_bonds_value_history and isinstance(game.stocks_bonds_value_history[-1], (int, float)) else stocks_bonds_total_value
            profit_loss = today_value - yesterday_value
            color = Fore.GREEN if profit_loss > 0 else (Fore.RED if profit_loss < 0 else Style.RESET_ALL)
            print(f"")
        else:
            print("")  # 如果没有历史数据，则换行
        total_assets_display = cash_display + stocks_bonds_total_value
        print(f"总资产：{total_assets_display:.2f}元")
        print(f"游戏天数：{game.day}")

        print("\n1. 股票交易")
        print("2. 债券市场")
        print("3. 查看持仓")
        print("4. 进入下一天")
        print("5. 查看交易历史")
        print("6. 查看资产价格走势图")
        print("7. 自动筛选好投资")
        print("8. 存档管理")
        print("9. 保存并退出")

        choice = input("请选择操作：")

        if choice == "1":
            game.bulk_stock_trade()
        elif choice == "2":
            game.show_bond_market()
            action = input("1.买入 2.卖出 3.返回：")
            if action == "1":
                game.buy_bonds()
            elif action == "2":
                game.sell_bonds()
        elif choice == "3":
            game.show_portfolio()
        elif choice == "4":
            game.daily_update()
            # 在每日更新后保存股票和债券总价值的历史记录
            stocks_bonds_total_value = 0.0
            stocks_dict = game.player.get('stocks', {})
            if isinstance(stocks_dict, dict):
                for code, holding_data in stocks_dict.items():
                    if isinstance(holding_data, dict) and isinstance(holding_data.get("amount"), (int, float)):
                        stock = game.market.stock_dict.get(code)
                        if stock:
                            stocks_bonds_total_value += float(stock.current_price) * float(holding_data["amount"])
            bonds_dict = game.player.get('bonds', {})
            if isinstance(bonds_dict, dict):
                for code, holding_data in bonds_dict.items():
                    if isinstance(holding_data, dict) and isinstance(holding_data.get("amount"), (int, float)):
                        bond = game.market.bond_dict.get(code)
                        if bond:
                            stocks_bonds_total_value += float(bond.current_price) * float(holding_data["amount"])
            game.stocks_bonds_value_history.append(stocks_bonds_total_value)
            if len(game.stocks_bonds_value_history) > 365:  # 保留一年数据
                game.stocks_bonds_value_history.pop(0)
            game.save_game()
        elif choice == "5":
            game.show_trade_history()
        elif choice == "6":
            # 在显示走势图前列出资产列表
            print(f"\n{Fore.YELLOW}=== 可查看资产列表 ==={Style.RESET_ALL}")
            print(f"{Fore.CYAN}--- 股票 ---{Style.RESET_ALL}")
            for stock in game.market.stocks:
                print(f"  {stock.code}: {stock.name}")
            print(f"{Fore.CYAN}--- 债券 ---{Style.RESET_ALL}")
            for bond in game.market.bonds:
                print(f"  {bond.code}: {bond.name}")
            print("-" * 30)
            game.show_horizontal_chart()
        elif choice == "7":
            game.screen_good_investments()  # 确保正确调用筛选功能
        elif choice == "8":
            manage_saves(game)
        elif choice == "9":
            game.save_game()
            print(f"{Fore.GREEN}游戏已保存，再见！{Style.RESET_ALL}")
            break
        else:
            print("无效输入！")

def select_save():
    """启动时选择存档"""
    if not os.path.exists('saves'):
        os.makedirs('saves')
    
    save_files = [f for f in os.listdir('saves') if f.endswith('.json')]
    print(f"\n{Fore.CYAN}=== 存档选择 ==={Style.RESET_ALL}")
    
    if not save_files:
        print("暂无存档，创建新存档")
        while True:
            new_name = input("请输入新存档名称（无需扩展名）: ").strip()
            if new_name:
                return f"{new_name}.json"
            print("名称不能为空")
    
    print("请选择存档：")
    for idx, save in enumerate(save_files):
        print(f"{idx+1}. {save}")
    print(f"{len(save_files)+1}. 新建存档")
    
    while True:
        choice = input("请输入选择（数字）: ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(save_files):
                return save_files[choice-1]
            elif choice == len(save_files)+1:
                while True:
                    new_name = input("请输入新存档名称（无需扩展名）: ").strip()
                    if new_name:
                        return f"{new_name}.json"
                    print("名称不能为空")
        print("输入无效，请重新输入")

def manage_saves(game):
    """存档管理子菜单"""
    while True:
        print(f"\n{Fore.CYAN}=== 存档管理 ==={Style.RESET_ALL}")
        print("1. 保存当前进度")
        print("2. 另存为新存档")
        print("3. 加载其他存档")
        print("4. 删除存档")
        print(f"5. 土豪模式: {'开启' if game.tycoon_mode else '关闭'}") # 直接显示当前状态，不显示锁定
        print("6. 返回主菜单")
        
        choice = input("请选择操作：")
        
        if choice == '1':
            game.save_game()
            print(f"{Fore.GREEN}当前进度已保存至 {game.current_save}{Style.RESET_ALL}")
        
        elif choice == '2':
            new_name = input("请输入新存档名称（无需扩展名）: ").strip()
            if new_name:
                new_save = f"{new_name}.json"
                old_save = game.current_save
                
                game.current_save = new_save
                game.save_game()
                
                switch = input(f"是否切换到新存档 {new_save}？(y/n): ").lower()
                if switch == 'y':
                    print(f"{Fore.GREEN}已切换到 {new_save}{Style.RESET_ALL}")
                else:
                    game.current_save = old_save
                continue
            print(f"{Fore.RED}无效的存档名称{Style.RESET_ALL}")
        
        elif choice == '3':
            saves = [f for f in os.listdir('saves') if f.endswith('.json')]
            if not saves:
                print(f"{Fore.YELLOW}暂无其他存档{Style.RESET_ALL}")
                continue
            
            print(f"\n{Fore.CYAN}=== 可用存档 ==={Style.RESET_ALL}")
            for idx, save in enumerate(saves):
                print(f"{idx+1}. {save}")
            print("0. 取消")
            
            load_choice = input("请选择要加载的存档（数字）: ").strip()
            if load_choice == '0':
                continue
            if not load_choice.isdigit():
                print(f"{Fore.RED}请输入数字{Style.RESET_ALL}")
                continue
            
            load_choice = int(load_choice)
            if 1 <= load_choice <= len(saves):
                selected = saves[load_choice-1]
                
                save_current = input("是否先保存当前进度？(y/n): ").lower()
                if save_current == 'y':
                    game.save_game()
                
                game.current_save = selected
                game.load_game()
                print(f"{Fore.GREEN}已加载存档 {selected}{Style.RESET_ALL}")
                return
            print(f"{Fore.RED}无效的选择{Style.RESET_ALL}")
        
        elif choice == '4':
            saves = [f for f in os.listdir('saves') if f.endswith('.json')]
            if not saves:
                print(f"{Fore.YELLOW}暂无存档可删除{Style.RESET_ALL}")
                continue
            
            print(f"\n{Fore.CYAN}=== 删除存档 ==={Style.RESET_ALL}")
            for idx, save in enumerate(saves):
                print(f"{idx+1}. {save}")
            print("0. 取消")
            
            del_choice = input("请选择要删除的存档（数字）: ").strip()
            if del_choice == '0':
                continue
            if not del_choice.isdigit():
                print(f"{Fore.RED}请输入数字{Style.RESET_ALL}")
                continue
            
            del_choice = int(del_choice)
            if 1 <= del_choice <= len(saves):
                selected = saves[del_choice-1]
                confirm = input(f"确认删除存档 {selected}？此操作不可恢复！(y/n): ").lower()
                if confirm == 'y':
                    try:
                        os.remove(os.path.join('saves', selected))
                        print(f"{Fore.GREEN}存档 {selected} 已删除{Style.RESET_ALL}")
                        if selected == game.current_save:
                            game.current_save = 'default_save.json'
                            print(f"{Fore.YELLOW}当前存档已重置为默认存档{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}删除失败：{str(e)}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}无效的选择{Style.RESET_ALL}")
        
        elif choice == '5':
            game.toggle_tycoon_mode()
        
        elif choice == '6':
            return
        
        else:
            print(f"{Fore.RED}无效的输入{Style.RESET_ALL}")

if __name__ == "__main__":
    save_file = select_save()
    game = StockTycoon(save_file)
    main_menu(game)
