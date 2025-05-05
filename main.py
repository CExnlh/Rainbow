import random
import time
import json
import shutil
from datetime import datetime
from colorama import Fore, Style

# ========== 数据模型 ==========
class Asset:
    def __init__(self, code, name, base_price, volatility, income):
        self.code = code
        self.name = name
        self.base_price = max(base_price, 10000)  # 确保基础价格有效
        self.current_price = self.base_price
        self.volatility = volatility
        self.income = income
        self.history = [self.base_price]

class Bond:
    def __init__(self, code, name, price, yield_rate, duration):
        self.code = code
        self.name = name
        self.price = price
        self.current_price = max(price, 5000)
        self.yield_rate = yield_rate
        self.duration = duration
        self.history = [self.current_price]

    def update_price(self):
        """债券价格波动（带价格保护）"""
        self.current_price = int(self.current_price * random.uniform(0.98, 1.02))
        self.current_price = max(self.current_price, 5000)
        self.history.append(self.current_price)
        if len(self.history) > 60:
            self.history.pop(0)

# ========== 游戏系统 ==========
class SeasonSystem:
    SEASONS = [
        {"name": "春", "stock_vol": 1.2, "bond_yield": 0.95},
        {"name": "夏", "stock_vol": 1.5, "bond_yield": 1.0},
        {"name": "秋", "stock_vol": 0.8, "bond_yield": 1.1},
        {"name": "冬", "stock_vol": 1.0, "bond_yield": 1.05}
    ]
    
    def __init__(self):
        self.start_day = datetime.now().toordinal()
    
    def current_season(self):
        days_passed = datetime.now().toordinal() - self.start_day
        return self.SEASONS[days_passed // 7 % 4]

class FinancialMarket:
    def __init__(self):
        self.stocks = self.generate_random_stocks()
        self.bonds = [
            Bond("GOV01", "国债-3月期", 10_000, 0.03, 90),
            Bond("GOV02", "国债-1年期", 10_000, 0.035, 365)
        ]
        self.stock_dict = {s.code: s for s in self.stocks}
        self.bond_dict = {b.code: b for b in self.bonds}
        self.day = 0

    def set_day(self, day):
        self.day = day

    def generate_random_stocks(self):
        """随机生成股票数据"""
        stock_templates = [
            ("APLE", "平果", 0.12, 300),
            ("GGLE", "古歌", 0.15, 400),
            ("HUAW", "化为", 0.18, 280),
            ("XIAM", "肖米", 0.2, 150),
            ("HONR", "容耀", 0.22, 180),
            ("FSSC", "富士糠", 0.16, 250),
            ("META", "麦塔", 0.25, 350),
            ("CGPT", "拆既", 0.3, 500),
            ("TWTE", "退特", 0.28, 320),
            ("VANK", "晚科", 0.2, 200)
        ]
        stocks = []
        for code, name, vol, income in stock_templates:
            base_price = random.randint(5000, 20000) * 10000
            stocks.append(Asset(code, name, base_price, vol, income))
        return stocks

    def update_stocks(self, season_mod):
        """更新股票价格（带波动限制和价格保护）"""
        for stock in self.stocks:
            # 计算基础波动
            base_change = random.gauss(0, 1) * stock.volatility * season_mod
            
            # 限制波动幅度在±50%之间
            clamped_change = max(min(base_change, 0.5), -0.5)
            
            # 计算新价格
            new_price = int(stock.current_price * (1 + clamped_change))
            
            # 价格保护：不低于基准价的20%
            price_floor = stock.base_price // 5
            stock.current_price = max(new_price, price_floor)
            
            # 维护价格历史
            stock.history.append(stock.current_price)
            if len(stock.history) > 60:
                stock.history.pop(0)

    def update_bonds(self, season_mod):
        for bond in self.bonds:
            change = random.gauss(0, 0.05) * season_mod["bond_yield"]
            new_price = int(bond.current_price * (1 + change))
            bond.current_price = max(new_price, 5000)
            bond.history.append(bond.current_price)
            if len(bond.history) > 60:
                bond.history.pop(0)

# ========== 核心游戏类 ==========
class StockTycoon:
    def __init__(self):
        self.player = {
            "cash": 10_000_000_000_000,
            "debt": 1_000_000_000_000,
            "stocks": {},     # 正常持仓
            "bonds": {},      # 债券持仓
            "shorts": {}      # 新增做空持仓 {代码: [数量, 借入价格, 借入天数]}
        }
        self.market = FinancialMarket()
        self.season = SeasonSystem()
        self.day = 0
        self.total_assets_history = []
        self.load_game()

    def load_game(self):
        """加载游戏存档"""
        try:
            with open('game_save.json', 'r') as f:
                data = json.load(f)
                self.player = data.get('player', self.player)
                self.day = data.get('day', 0)
                # 加载其他游戏数据
        except FileNotFoundError:
            print("没有找到存档，使用默认值开始游戏")
        except json.JSONDecodeError:
            print("存档文件损坏，使用默认值开始游戏")

    def save_game(self):
        """保存游戏进度"""
        data = {
            'player': self.player,
            'day': self.day
        }
        with open('game_save.json', 'w') as f:
            json.dump(data, f, indent=2)
        print("游戏进度已保存")

    def calculate_total_assets(self) -> int:
        """计算玩家总资产"""
        total = self.player.get('cash', 0)
        # 计算股票价值
        stocks_dict = self.player.get('stocks', {})
        if isinstance(stocks_dict, dict):
            for code, amount in stocks_dict.items():
                stock = self.market.stock_dict.get(code)
                if stock and isinstance(amount, (int, float)):
                    total += stock.current_price * amount
        # 计算债券价值
        bonds_dict = self.player.get('bonds', {})
        if isinstance(bonds_dict, dict):
            for code, amount in bonds_dict.items():
                bond = self.market.bond_dict.get(code)
                if bond and isinstance(amount, (int, float)):
                    total += bond.current_price * amount
        return int(total)

    def show_stock_market(self):
        """显示股票市场信息"""
        print(f"{Fore.CYAN}=== 股票市场 ==={Style.RESET_ALL}")
        print(f"当前第 {self.day} 天")
        season = self.season.current_season()
        print(f"当前季节：{season['name']} (股票波动：{season['stock_vol']:.1f}x)")
        print("代码 | 名称 | 当前价格(元) | 波动性")
        print("-" * 40)
        for stock in self.market.stocks:
            price_wan = stock.current_price / 10000.0
            print(f"{stock.code} | {stock.name} | {price_wan:.2f} | {stock.volatility:.2f}")

    def show_bond_market(self):
        """显示债券市场信息"""
        print(f"{Fore.CYAN}=== 债券市场 ==={Style.RESET_ALL}")
        print(f"当前第 {self.day} 天")
        season = self.season.current_season()
        print(f"当前季节：{season['name']} (债券收益：{season['bond_yield']:.1f}x)")
        print("代码 | 名称 | 当前价格(元) | 年化收益率 | 期限(天)")
        print("-" * 50)
        for bond in self.market.bonds:
            price_wan = bond.current_price / 10000.0
            yield_pct = bond.yield_rate * 100
            print(f"{bond.code} | {bond.name} | {price_wan:.2f} | {yield_pct:.1f}% | {bond.duration}")

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
        except ValueError:
            print("无效的数量")
            return
            
        total_cost = bond.current_price * amount
        current_cash = self.player.get('cash', 0)
        if total_cost > current_cash:
            print("资金不足")
            return
            
        self.player['cash'] = current_cash - total_cost
        bonds = self.player.get('bonds', {})
        if isinstance(bonds, dict):
            current_amount = bonds.get(code, 0)
            if isinstance(current_amount, (int, float)):
                bonds[code] = current_amount + amount
            else:
                bonds[code] = amount
            self.player['bonds'] = bonds
        print(f"成功购买 {amount} 单位 {bond.name}")

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
        if isinstance(bonds, dict):
            current_amount = bonds.get(code, 0)
            
            if current_amount <= 0:
                print(f"{Fore.RED}错误：没有该债券持仓{Style.RESET_ALL}")
                return
            
            try:
                sell_amount = int(input(f"请输入卖出数量（当前持仓：{current_amount}）："))
                if sell_amount <= 0 or sell_amount > current_amount:
                    raise ValueError
            except:
                print(f"{Fore.RED}错误：无效的数量{Style.RESET_ALL}")
                return
            
            # 计算收益
            total = bond.current_price * sell_amount
            self.player["cash"] = self.player.get("cash", 0) + total
            
            # 更新持仓
            bonds[code] = current_amount - sell_amount
            if bonds[code] == 0:
                del bonds[code]
            self.player["bonds"] = bonds
            
            print(f"{Fore.GREEN}成功卖出 {sell_amount} 单位 {bond.name}，获得{total/10000:.2f}元{Style.RESET_ALL}")
            self.save_game()

    def short_stock(self):
        """股票做空功能"""
        self.show_stock_market()
        code = input("输入要做空的股票代码：").upper()
        
        if code not in self.market.stock_dict:
            print(f"{Fore.RED}错误：无效的股票代码{Style.RESET_ALL}")
            return
            
        stock = self.market.stock_dict[code]
        
        try:
            amount = int(input(f"做空数量（当前价：{stock.current_price/10000:.2f}元/股）："))
            if amount <= 0:
                raise ValueError
        except:
            print(f"{Fore.RED}错误：无效的数量{Style.RESET_ALL}")
            return
            
        # 计算保证金（假设50%保证金率）
        margin_required = stock.current_price * amount * 0.5
        if self.player.get("cash", 0) < margin_required:
            print(f"{Fore.RED}错误：保证金不足，需要{margin_required/10000:.2f}元{Style.RESET_ALL}")
            return
            
        # 记录做空仓位
        current_cash = self.player.get("cash", 0)
        self.player["cash"] = current_cash + stock.current_price * amount - margin_required
        
        shorts = self.player.get("shorts", {})
        if isinstance(shorts, dict):
            short_data = [
                amount, 
                stock.current_price,
                self.day  # 记录借入天数
            ]
            shorts[code] = short_data
            self.player["shorts"] = shorts
        print(f"{Fore.GREEN}成功做空 {amount} 股 {stock.name}，保证金已扣除{Style.RESET_ALL}")
        self.save_game()

    def cover_short(self):
        """平仓做空仓位"""
        shorts = self.player.get("shorts", {})
        if not isinstance(shorts, dict) or not shorts:
            print(f"{Fore.YELLOW}当前没有做空仓位{Style.RESET_ALL}")
            return
            
        print(f"{Fore.CYAN}=== 做空仓位 ==={Style.RESET_ALL}")
        for code, data in shorts.items():
            stock = self.market.stock_dict.get(code)
            current_price = stock.current_price if stock else 0
            print(f"代码：{code} 数量：{data[0]} 盈亏：{(data[1]-current_price)*data[0]/10000:.2f}元")
            
        code = input("输入要平仓的股票代码：").upper()
        if code not in shorts:
            print(f"{Fore.RED}错误：没有该股票的做空仓位{Style.RESET_ALL}")
            return
            
        short_data = shorts[code]
        stock = self.market.stock_dict[code]
        
        # 计算买回成本
        buyback_cost = stock.current_price * short_data[0]
        if self.player.get("cash", 0) < buyback_cost:
            print(f"{Fore.RED}错误：现金不足，需要{buyback_cost/10000:.2f}元{Style.RESET_ALL}")
            return
            
        # 计算盈亏
        profit = (short_data[1] - stock.current_price) * short_data[0]
        current_cash = self.player.get("cash", 0)
        self.player["cash"] = current_cash + profit + short_data[0] * short_data[1] * 0.5
        
        # 移除仓位
        del shorts[code]
        self.player["shorts"] = shorts
        print(f"{Fore.GREEN}平仓成功，净盈亏：{profit/10000:.2f}元{Style.RESET_ALL}")
        self.save_game()

    def show_portfolio(self):
        """显示玩家投资组合（增加做空仓位显示）"""
        print(f"{Fore.CYAN}=== 我的持仓 ==={Style.RESET_ALL}")
        cash = self.player.get('cash', 0)
        debt = self.player.get('debt', 0)
        print(f"现金：{float(cash)/10000.0:.2f}元")
        print(f"债务：{float(debt)/10000.0:.2f}元")
        total_stock_value = 0
        print("\n股票持仓：")
        print("代码 | 名称 | 数量 | 当前价(元) | 总价值(元)")
        print("-" * 40)
        stocks = self.player.get('stocks', {})
        if isinstance(stocks, dict):
            for code, amount in stocks.items():
                stock = self.market.stock_dict.get(code)
                if stock and isinstance(amount, (int, float)):
                    value = stock.current_price * amount
                    total_stock_value += value
                    print(f"{code} | {stock.name} | {amount} | {stock.current_price/10000.0:.2f} | {value/10000.0:.2f}")
        if not stocks or not isinstance(stocks, dict) or not stocks.items():
            print("(空)")
            
        total_bond_value = 0
        print("\n债券持仓：")
        print("代码 | 名称 | 数量 | 当前价(元) | 总价值(元)")
        print("-" * 40)
        bonds = self.player.get('bonds', {})
        if isinstance(bonds, dict):
            for code, amount in bonds.items():
                bond = self.market.bond_dict.get(code)
                if bond and isinstance(amount, (int, float)):
                    value = bond.current_price * amount
                    total_bond_value += value
                    print(f"{code} | {bond.name} | {amount} | {bond.current_price/10000.0:.2f} | {value/10000.0:.2f}")
        if not bonds or not isinstance(bonds, dict) or not bonds.items():
            print("(空)")
            
        # 显示做空仓位
        print(f"\n{Fore.RED}=== 做空仓位 ==={Style.RESET_ALL}")
        shorts = self.player.get("shorts", {})
        if not isinstance(shorts, dict) or not shorts:
            print("当前没有做空仓位")
        else:
            print("代码 | 名称 | 数量 | 借入价格 | 当前价格 | 盈亏")
            print("-" * 60)
            for code, data in shorts.items():
                stock = self.market.stock_dict.get(code)
                current_price = stock.current_price if stock else 0
                profit = (data[1] - current_price) * data[0]
                print(f"{code} | {stock.name if stock else '未知'} | {data[0]} | {data[1]/10000:.2f}元 | {current_price/10000:.2f}元 | {profit/10000:.2f}元")
        
        total_assets = cash + total_stock_value + total_bond_value
        print(f"\n总资产：{float(total_assets)/10000.0:.2f}元")
        print(f"净资产：{float(total_assets - debt)/10000.0:.2f}元")

    def show_asset_trend(self):
        """显示资产趋势"""
        print(f"{Fore.CYAN}=== 资产趋势 ==={Style.RESET_ALL}")
        if not self.total_assets_history:
            print("暂无历史数据")
            return
            
        max_days = min(30, len(self.total_assets_history))
        history = self.total_assets_history[-max_days:]
        min_val = min(history)
        max_val = max(history)
        if max_val == min_val:
            max_val = min_val + 1
            
        term_width = shutil.get_terminal_size().columns
        chart_width = min(60, term_width - 20)
        
        print(f"近 {max_days} 天资产趋势 (单位：元)")
        print(f"范围：{min_val/10000.0:.2f}元 ~ {max_val/10000.0:.2f}元")
        
        for i, val in enumerate(history):
            norm_val = (val - min_val) / (max_val - min_val)
            bar_len = int(norm_val * chart_width)
            day_num = self.day - len(history) + i + 1
            color = Fore.GREEN if i > 0 and val >= history[i-1] else Fore.RED
            print(f"第{day_num:3d}天 | {color}{'█' * bar_len}{Style.RESET_ALL} {val/10000.0:.2f}")

    def show_horizontal_chart(self):
        """优化后的水平走势图显示（完整修复版）"""
        print("\n=== 资产走势分析 ===")
        code = input("请输入资产代码：").upper()
        asset = self.market.stock_dict.get(code) or self.market.bond_dict.get(code)
        
        if not asset or not asset.history:
            print("无效资产代码或没有历史数据")
            return

        # 动态终端适配
        term_width, _ = shutil.get_terminal_size()
        max_bar_width = max(30, term_width - 35)  # 为价格标签留出空间
        max_days = min(60, max_bar_width // 4)
        
        # 获取历史数据（最近max_days天）
        history = asset.history[-max_days:]
        day_count = len(history)
        start_day = self.day - day_count + 1
        
        # 计算显示参数
        min_price = min(history)
        max_price = max(history)
        price_range = max(max_price - min_price, 1)  # 防止除零

        # 打印头部信息
        print(f"\n{asset.name} ({code}) 近期走势".center(term_width))
        print(f"当前第 {self.day} 天 | 显示 {day_count} 个交易日".center(term_width))
        print(f"历史价格范围：{min_price/10000:.2f}元 ~ {max_price/10000:.2f}元".center(term_width))
        
        # 绘制走势图
        for idx in range(day_count):
            current_price = history[idx]
            prev_price = history[idx-1] if idx > 0 else current_price
            
            # 计算进度比例（至少显示1个字符）
            progress = (current_price - min_price) / price_range
            bar_width = max(1, int(progress * max_bar_width))  # 确保最小显示宽度
            
            # 确定颜色
            if idx == 0:
                color = Style.RESET_ALL  # 首日默认颜色
            else:
                color = Fore.GREEN if current_price >= prev_price else Fore.RED
            
            # 构建显示元素
            bar = f"{color}█" * bar_width
            price_label = f"{Style.RESET_ALL}{current_price/10000:>8.2f}元"
            day_label = f" (第{start_day + idx}天)" if idx % 5 == 0 or idx == day_count-1 else ""
            
            # 格式化输出
            line = f"{bar}{price_label}{day_label}"
            print(line.ljust(term_width))  # 确保对齐终端右边界

        # 图例说明
        print(f"\n{Fore.YELLOW}图例说明：")
        print(f"███绿色：当日价格上涨 | ███红色：当日价格下跌 | ███白色：首日基准")
        print(f"* 每5天显示日期标签，最后一天强制显示")
        print(f"* 柱状长度反映相对价格区间，非绝对涨跌幅{Style.RESET_ALL}")

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
        
        try:
            # 获取并验证交易数量
            if action in ["1", "2", "3"]:
                amount = int(input(f"操作数量（当前价：{stock.current_price/10000:.2f}元/股）："))
                if amount <= 0:
                    raise ValueError("数量必须为正整数")
        except ValueError as e:
            print(f"{Fore.RED}错误：{e}{Style.RESET_ALL}")
            return
        
        # 买入逻辑
        if action == "1":
            total_cost = stock.current_price * amount
            current_cash = self.player.get("cash", 0)
            if total_cost > current_cash:
                print(f"{Fore.RED}错误：资金不足，需要{total_cost/10000:.2f}元{Style.RESET_ALL}")
            else:
                self.player["cash"] = current_cash - total_cost
                stocks = self.player.get("stocks", {})
                if isinstance(stocks, dict):
                    current_holding = stocks.get(code, 0)
                    stocks[code] = current_holding + amount
                    self.player["stocks"] = stocks
                print(f"{Fore.GREEN}成功买入 {amount} 股 {stock.name}{Style.RESET_ALL}")
        
        # 卖出逻辑
        elif action == "2":
            stocks = self.player.get("stocks", {})
            if isinstance(stocks, dict):
                current_holding = stocks.get(code, 0)
                
                # 强化类型检查
                if not isinstance(current_holding, (int, float)) or current_holding < amount:
                    print(f"{Fore.RED}错误：持仓不足，当前持有 {current_holding} 股{Style.RESET_ALL}")
                    return
                
                # 计算收益
                total_income = stock.current_price * amount
                self.player["cash"] = self.player.get("cash", 0) + total_income
                
                # 更新持仓
                new_holding = current_holding - amount
                if new_holding > 0:
                    stocks[code] = new_holding
                else:
                    if code in stocks:
                        del stocks[code]  # 完全卖出后移除持仓记录
                self.player["stocks"] = stocks
                
                print(f"{Fore.GREEN}成功卖出 {amount} 股 {stock.name}，获得{total_income/10000:.2f}元{Style.RESET_ALL}")
        
        # 做空逻辑
        elif action == "3":
            # 计算保证金（假设50%保证金率）
            margin_required = stock.current_price * amount * 0.5
            current_cash = self.player.get("cash", 0)
            if current_cash < margin_required:
                print(f"{Fore.RED}错误：保证金不足，需要{margin_required/10000:.2f}元{Style.RESET_ALL}")
                return
            
            # 记录做空仓位
            self.player["cash"] = current_cash + stock.current_price * amount - margin_required
            shorts = self.player.get("shorts", {})
            if isinstance(shorts, dict):
                short_data = [
                    amount, 
                    stock.current_price,
                    self.day  # 记录借入天数
                ]
                shorts[code] = short_data
                self.player["shorts"] = shorts
            print(f"{Fore.GREEN}成功做空 {amount} 股 {stock.name}，保证金已扣除{Style.RESET_ALL}")
        
        # 平仓做空逻辑
        elif action == "4":
            shorts = self.player.get("shorts", {})
            if isinstance(shorts, dict):
                if code not in shorts:
                    print(f"{Fore.RED}错误：没有该股票的做空仓位{Style.RESET_ALL}")
                    return
                
                short_data = shorts[code]
                
                # 计算买回成本
                buyback_cost = stock.current_price * short_data[0]
                current_cash = self.player.get("cash", 0)
                if current_cash < buyback_cost:
                    print(f"{Fore.RED}错误：现金不足，需要{buyback_cost/10000:.2f}元{Style.RESET_ALL}")
                    return
                
                # 计算盈亏
                profit = (short_data[1] - stock.current_price) * short_data[0]
                self.player["cash"] = current_cash + profit + short_data[0] * short_data[1] * 0.5
                
                # 移除仓位
                if code in shorts:
                    del shorts[code]
                self.player["shorts"] = shorts
                print(f"{Fore.GREEN}平仓成功，净盈亏：{profit/10000:.2f}元{Style.RESET_ALL}")
        
        else:
            print(f"{Fore.RED}错误：无效的操作选择{Style.RESET_ALL}")
            return
        
        self.save_game()

    def daily_update(self):
        """增强的每日结算"""
        self.day += 1
        self.market.set_day(self.day)
        season = self.season.current_season()
        
        # 并行更新股票和债券
        self.market.update_stocks(season["stock_vol"])
        self.market.update_bonds(season)
        
        # 其余结算逻辑保持不变
        # ...

# ========== 主菜单 ==========
def main_menu(game):
    while True:
        print(f"\n{Fore.CYAN}=== 主菜单 ===")
        print(f"现金：{game.player['cash']/10000:.2f}元")
        print(f"债务：{game.player['debt']/10000:.2f}元")
        print(f"总资产：{game.calculate_total_assets()/10000:.2f}元")
        print(f"游戏天数：{game.day}{Style.RESET_ALL}")
        
        print("\n1. 股票交易")
        print("2. 债券市场")
        print("3. 查看持仓")
        print("4. 查看资产走势")
        print("5. 进入下一天")
        print("6. 查看水平走势图")
        print("7. 保存退出")
        
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
            game.show_asset_trend()
        elif choice == "5":
            game.daily_update()
        elif choice == "6":
            game.show_horizontal_chart()
        elif choice == "7":
            game.save_game()
            print("游戏已保存，再见！")
            break
        else:
            print("无效输入！")

if __name__ == "__main__":
    game = StockTycoon()
    main_menu(game)
