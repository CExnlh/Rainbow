import random
import time
import json
from datetime import datetime
from colorama import Fore, Style

# ========== 数据模型 ==========
class Asset:
    def __init__(self, code, name, base_price, volatility, income):
        self.code = code
        self.name = name
        self.base_price = base_price
        self.current_price = base_price
        self.volatility = volatility
        self.income = income
        self.history = [base_price]  # 价格历史

class Player:
    def __init__(self):
        self.cash = 10_000_000_000_000  # 初始资金
        self.debt = 1_000_000_000_000   # 初始债务
        self.portfolio = {}  # {资产代码: 持有数量}

# ========== 游戏系统 ==========
class SeasonSystem:
    SEASONS = [
        {"name": "春", "lottery_mult": 1.2, "asset_vol": 1.2},
        {"name": "夏", "lottery_mult": 0.9, "asset_vol": 0.8},
        {"name": "秋", "lottery_mult": 1.5, "asset_vol": 1.5},
        {"name": "冬", "lottery_mult": 0.8, "asset_vol": 1.0}
    ]
    
    def __init__(self):
        self.start_day = datetime.now().toordinal()
    
    def current_season(self):
        days_passed = datetime.now().toordinal() - self.start_day
        return self.SEASONS[days_passed // 7 % 4]

class AssetMarket:
    ASSET_DATA = [
        ("RE01", "数字地产", 5_000_000, 0.15, 300_000),
        ("TECH01", "量子计算", 20_000_000, 0.35, 1_500_000),
        ("LUX01", "太空游艇", 50_000_000, 0.25, 3_000_000),
        ("CUL01", "元宇宙画廊", 3_000_000, 0.4, 200_000)
    ]
    
    def __init__(self):
        self.assets = {data[0]: Asset(*data) for data in self.ASSET_DATA}
    
    def update_prices(self, season_mod):
        """更新资产价格（带季节波动）"""
        for asset in self.assets.values():
            change = random.uniform(-1, 1) * asset.volatility * season_mod
            new_price = int(asset.current_price * (1 + change))
            asset.current_price = new_price
            asset.history.append(new_price)
            if len(asset.history) > 30:
                asset.history.pop(0)

# ========== 核心游戏 ==========
class RainbowGame:
    def __init__(self):
        self.player = Player()
        self.season = SeasonSystem()
        self.market = AssetMarket()
        self.day = 0
        self.load_game()
    
    # ========== 存档系统 ==========
    def save_game(self):
        data = {
            "cash": self.player.cash,
            "debt": self.player.debt,
            "day": self.day,
            "portfolio": self.player.portfolio,
            "assets": {code: a.__dict__ for code, a in self.market.assets.items()}
        }
        with open("save.json", "w") as f:
            json.dump(data, f)
        print(f"{Fore.GREEN}游戏已保存！{Style.RESET_ALL}")
    
    def load_game(self):
        try:
            with open("save.json") as f:
                data = json.load(f)
                self.player.cash = data["cash"]
                self.player.debt = data["debt"]
                self.day = data["day"]
                self.player.portfolio = data["portfolio"]
                for code, asset_data in data["assets"].items():
                    a = self.market.assets[code]
                    a.current_price = asset_data["current_price"]
                    a.history = asset_data["history"]
            print(f"{Fore.CYAN}存档加载成功！{Style.RESET_ALL}")
        except:
            print(f"{Fore.YELLOW}新建游戏启动{Style.RESET_ALL}")

    # ========== 资产交易 ==========
    def buy_assets(self):
        """批量购买资产"""
        self.show_market()
        code = input("输入资产代码：").upper()
        if code not in self.market.assets:
            print("无效代码！")
            return
        
        asset = self.market.assets[code]
        try:
            amount = int(input(f"购买数量（当前价格：{asset.current_price//10000}万/份）："))
            if amount <= 0:
                raise ValueError
        except:
            print("无效数量！")
            return
        
        total_cost = asset.current_price * amount
        if total_cost > self.player.cash:
            print(f"{Fore.RED}资金不足！需要{total_cost//10000}万{Style.RESET_ALL}")
            return
        
        self.player.cash -= total_cost
        self.player.portfolio[code] = self.player.portfolio.get(code, 0) + amount
        print(f"成功购买{asset.name} ×{amount}")
        self.save_game()

    def sell_assets(self):
        """批量卖出资产"""
        if not self.player.portfolio:
            print("没有持有任何资产！")
            return
        
        self.show_portfolio()
        code = input("输入要卖出的资产代码：").upper()
        if code not in self.player.portfolio:
            print("未持有该资产！")
            return
        
        asset = self.market.assets[code]
        try:
            amount = int(input(f"卖出数量（最多{self.player.portfolio[code]}份）："))
            if amount <= 0 or amount > self.player.portfolio[code]:
                raise ValueError
        except:
            print("无效数量！")
            return
        
        total = asset.current_price * amount
        self.player.cash += total
        self.player.portfolio[code] -= amount
        if self.player.portfolio[code] == 0:
            del self.player.portfolio[code]
        print(f"成功卖出{asset.name} ×{amount}，获得{total//10000}万")
        self.save_game()

    # ========== 彩票系统 ==========
    def bulk_lottery(self):
        """批量彩票投注"""
        try:
            tickets = int(input("请输入购买数量（每秒处理10万张）："))
            if tickets <= 0:
                raise ValueError
        except:
            print("无效输入！")
            return
        
        cost = tickets * 10
        if cost > self.player.cash:
            print(f"{Fore.RED}余额不足！{Style.RESET_ALL}")
            return
        
        season = self.season.current_season()
        print(f"{season['name']}季：收益系数{season['lottery_mult']}x")
        
        start_time = time.time()
        win_table = {1:0, 2:0, 3:0, 4:0, 5:0}
        
        # 批量处理
        for _ in range(tickets):
            user_num = f"{random.randint(0,99999):05d}"
            win_num = f"{random.randint(0,99999):05d}"
            matched = sum(u == w for u, w in zip(user_num, win_num))
            if matched in win_table:
                win_table[matched] += 1
        
        # 计算收益
        rewards = {1:1, 2:10, 3:100, 4:1000, 5:10000}
        total_win = sum(rewards[k]*v for k,v in win_table.items()) * season['lottery_mult']
        
        # 更新状态
        self.player.cash += (total_win - cost)
        print(f"\n耗时：{time.time()-start_time:.2f}秒")
        print(f"净收益：{Fore.GREEN}{total_win - cost:,}{Style.RESET_ALL}元")
        self.save_game()

    # ========== 每日结算 ==========
    def daily_update(self):
        """处理每日结算"""
        self.day += 1
        season = self.season.current_season()
        
        # 更新资产价格
        self.market.update_prices(season["asset_vol"])
        
        # 计算资产收益
        income = 0
        for code, amount in self.player.portfolio.items():
            income += self.market.assets[code].income * amount
        
        # 更新债务
        interest = int(self.player.debt * 0.0001)
        
        # 更新资金
        self.player.cash += income
        self.player.debt += interest
        
        print(f"\n{Fore.YELLOW}=== 第{self.day}日结算 ===")
        print(f"资产收益：+{income//10000}万")
        print(f"债务利息：+{interest//10000}万{Style.RESET_ALL}")
        self.save_game()

    # ========== 显示界面 ==========
    def show_market(self):
        """显示资产市场"""
        print(f"\n{Fore.MAGENTA}=== 资产市场 ===")
        print(f"{'代码':<6}{'名称':<12}{'价格(万)':<10}{'收益率%':<8}波动率")
        for code, asset in self.market.assets.items():
            price = asset.current_price // 10000
            yield_rate = (asset.income / asset.current_price) * 100
            vol_icon = "🌪️" if asset.volatility > 0.3 else "🌊"
            print(f"{code:<6}{asset.name:<12}{price:<10}{yield_rate:<8.1f}{vol_icon}{asset.volatility:.2f}")
        print(Style.RESET_ALL)

    def show_portfolio(self):
        """显示投资组合"""
        print(f"\n{Fore.CYAN}=== 资产组合 ===")
        print(f"现金：{self.player.cash//10000}万")
        print(f"债务：{self.player.debt//10000}万")
        total_value = self.player.cash
        for code, amount in self.player.portfolio.items():
            asset = self.market.assets[code]
            value = asset.current_price * amount
            total_value += value
            print(f"{code} {asset.name} ×{amount} 估值：{value//10000}万")
        print(f"总资产：{total_value//10000}万{Style.RESET_ALL}")

    def show_price_trend(self):
        """显示价格走势"""
        code = input("输入资产代码：").upper()
        if code not in self.market.assets:
            print("无效代码！")
            return
        
        asset = self.market.assets[code]
        print(f"\n{Fore.BLUE}=== {asset.name}价格走势 ===")
        prices = [p//10000 for p in asset.history[-10:]]
        max_p = max(prices) if prices else 1
        
        for p in prices:
            bar = "█" * int(p / max_p * 20)
            print(f"{p:5}万 | {Fore.GREEN}{bar}{Style.RESET_ALL}")

# ========== 主程序 ==========
def main():
    game = RainbowGame()
    
    while True:
        print(f"\n{Fore.BLUE}=== 主菜单 ===")
        print(f"游戏天数：{game.day}")
        print("1. 购买彩票")
        print("2. 资产市场")
        print("3. 我的资产")
        print("4. 买卖资产")
        print("5. 查看走势")
        print("6. 进入下一天")
        print("7. 保存退出")
        
        choice = input("请选择操作：")
        
        if choice == "1":
            game.bulk_lottery()
        elif choice == "2":
            game.show_market()
        elif choice == "3":
            game.show_portfolio()
        elif choice == "4":
            print("\n1.买入 2.卖出")
            sub = input("请选择：")
            if sub == "1":
                game.buy_assets()
            elif sub == "2":
                game.sell_assets()
        elif choice == "5":
            game.show_price_trend()
        elif choice == "6":
            game.daily_update()
        elif choice == "7":
            game.save_game()
            print("游戏已保存，再见！")
            break
        else:
            print("无效输入！")

if __name__ == "__main__":
    main()