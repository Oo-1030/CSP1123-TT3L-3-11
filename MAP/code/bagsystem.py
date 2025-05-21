import pygame

class BagSystem:
    def __init__(self, screen,item_descriptions):
        # ==================== 布局参数 ====================
        # 物品图标大小
        self.ITEM_ICON_SIZE = 64  # 统一控制图标大小
        
        # 格子布局参数
        self.GRID_COLS = 5         # 列数
        self.GRID_ROWS = 5         # 行数
        self.GRID_CELL_SIZE = 90   # 每个格子的大小（正方形）
        self.GRID_SPACING = 10     # 格子间距
        self.GRID_START_X = 400    # 起始X坐标
        self.GRID_START_Y = 120     # 起始Y坐标
        
        # ==================== 计算参数 ====================
        self.ITEMS_PER_PAGE = self.GRID_COLS * self.GRID_ROWS
        self.WINDOW_WIDTH = self.GRID_START_X * 2 + \
                           self.GRID_COLS * (self.GRID_CELL_SIZE + self.GRID_SPACING)
        self.WINDOW_HEIGHT = self.GRID_START_Y * 2 + \
                            self.GRID_ROWS * (self.GRID_CELL_SIZE + self.GRID_SPACING)
        
        # 背景参数
        self.BG_IMAGE = pygame.transform.scale(pygame.image.load('CSP1123-TT3L-3-11/MAP/images/Bag_background.png'), (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        
        # 文字参数
        self.PAGE_INFO_POS = (self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT-30)  # 页码位置
        
        # 使用传入的screen
        self.screen = screen
        
        # 字体设置
        self.font = pygame.font.Font(None, 20)
        self.description_font = pygame.font.Font(None, 20)

        
        # 状态变量
        self.bag_is_open = False
        self.current_page = 0
        # 添加描述框参数
        self.DESC_BOX_WIDTH = 300  # 描述框宽度
        self.DESC_BOX_PADDING = 15  # 描述框内边距
        self.DESC_LINE_SPACING = 5  # 行间距
        self.item_descriptions = item_descriptions
        

        # 物品分类字典 (按星级从高到低排序)
        self.item_categories = {
            5: ["Clover", "Black_card", "Underwear", "Koi_fish"],
            4: ["Umbrella", "Coupon", "Tissue"],
            3: ["Rice", "Coffee", "Full_mark", "Eraser", "Watch", "Cola"]
        }

        self.image_map = self._load_images()

        self.GRID_COLORS = {
            5: (255, 231, 186),  # 五星 - 浅金色
            4: (230, 204, 255),  # 四星 - 浅紫色
            3: (204, 229, 255),  # 三星 - 浅蓝色
            'empty': (240, 240, 240)  # 空格子 - 默认灰色
        }

    def _load_images(self):
        """加载所有物品图片"""
        def load_image(name):
            try:
                return pygame.transform.scale(
                    pygame.image.load(f"{name}.png"), 
                    (self.ITEM_ICON_SIZE, self.ITEM_ICON_SIZE)
                )
            except:
                # 创建一个带问号的占位图
                dummy = pygame.Surface((self.ITEM_ICON_SIZE, self.ITEM_ICON_SIZE))
                dummy.fill((220, 220, 220))
                pygame.draw.line(dummy, (150, 150, 150), (0, 0), (self.ITEM_ICON_SIZE, self.ITEM_ICON_SIZE), 2)
                pygame.draw.line(dummy, (150, 150, 150), (self.ITEM_ICON_SIZE, 0), (0, self.ITEM_ICON_SIZE), 2)
                text = self.font.render("?", True, (100, 100, 100))
                text_rect = text.get_rect(center=(self.ITEM_ICON_SIZE//2, self.ITEM_ICON_SIZE//2))
                dummy.blit(text, text_rect)
                return dummy
        
        # 从item_categories中加载所有物品图片
        image_map = {}
        for star_level, items in self.item_categories.items():
            for item in items:
                image_map[item] = load_image(item)
        return image_map

    def _process_inventory(self, inventory):
        """处理物品列表，统计数量和去重"""
        item_counts = {}
        for item in inventory:
            item_counts[item] = item_counts.get(item, 0) + 1
        
        # 按星级从高到低排序物品
        sorted_items = []
        for star_level in sorted(self.item_categories.keys(), reverse=True):
            for item in self.item_categories[star_level]:
                if item in item_counts:
                    sorted_items.append(item)
        
        return sorted_items, item_counts
    
    def _draw_grid(self, unique_items, item_counts):
        """绘制5x5格子及物品"""
        for row in range(self.GRID_ROWS):
            for col in range(self.GRID_COLS):
                # 计算格子位置
                x = self.GRID_START_X + col * (self.GRID_CELL_SIZE + self.GRID_SPACING)
                y = self.GRID_START_Y + row * (self.GRID_CELL_SIZE + self.GRID_SPACING)
                
                # 获取当前格子物品的星级 (新增)
                index = self.current_page * self.ITEMS_PER_PAGE + row * self.GRID_COLS + col
                if index < len(unique_items):
                    item = unique_items[index]
                    # 查找物品对应的星级
                    star_level = None
                    for level, items in self.item_categories.items():
                        if item in items:
                            star_level = level
                            break
                    grid_color = self.GRID_COLORS.get(star_level, self.GRID_COLORS['empty'])
                else:
                    grid_color = self.GRID_COLORS['empty']
                
                # 绘制格子背景 (修改)
                pygame.draw.rect(self.screen, grid_color, 
                               (x, y, self.GRID_CELL_SIZE, self.GRID_CELL_SIZE))
                pygame.draw.rect(self.screen, (200, 200, 200), 
                               (x, y, self.GRID_CELL_SIZE, self.GRID_CELL_SIZE), 2)
                
                # 绘制物品（如果有）
                if index < len(unique_items):
                    item = unique_items[index]
                    if item in self.image_map:
                        img = self.image_map[item]
                        # 居中显示图标
                        icon_x = x + (self.GRID_CELL_SIZE - self.ITEM_ICON_SIZE) // 2
                        icon_y = y + (self.GRID_CELL_SIZE - self.ITEM_ICON_SIZE) // 2
                        self.screen.blit(img, (icon_x, icon_y))
                        
                        # 绘制数量
                        if item_counts[item] > 1:
                            count_text = self.font.render(
                                f"x{item_counts[item]}", 
                                True, 
                                (255, 0, 0)
                            )
                            text_rect = count_text.get_rect(
                                bottomright=(x + self.GRID_CELL_SIZE-5, 
                                            y + self.GRID_CELL_SIZE-5)
                            )
                            self.screen.blit(count_text, text_rect)
    
    def _draw_page_info(self, total_pages):
        """绘制页码信息"""
        if total_pages > 1:
            page_text = self.font.render(
                f"Page {self.current_page+1}/{total_pages}", 
                True, 
                (0, 0, 0)
            )
            self.screen.blit(page_text, self.PAGE_INFO_POS)

    def _draw_description(self, item):
        """绘制物品描述"""
        if item not in self.item_descriptions:
            return
            
        # 计算描述框位置 (右侧)
        desc_box_x = self.GRID_START_X + self.GRID_COLS * (self.GRID_CELL_SIZE + self.GRID_SPACING) + 20
        desc_box_y = self.GRID_START_Y
        desc_box_height = 200  # 初始高度，会根据内容调整
        
        # 渲染描述文本
        description = self.item_descriptions[item]
        words = description.split(' ')
        font = self.description_font
        line_height = font.get_linesize()
        
        # 计算需要的行数和总高度
        current_line = []
        lines = []
        current_width = 0
        space_width = font.size(' ')[0]
        
        for word in words:
            word_width = font.size(word)[0]
            if current_width + (len(current_line) > 0) * space_width + word_width <= self.DESC_BOX_WIDTH - 2 * self.DESC_BOX_PADDING:
                current_line.append(word)
                current_width += (len(current_line) > 1) * space_width + word_width
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width
                
        if current_line:
            lines.append(' '.join(current_line))
        
        # 更新描述框高度
        desc_box_height = len(lines) * line_height + 2 * self.DESC_BOX_PADDING + (len(lines) - 1) * self.DESC_LINE_SPACING + 25
        
        # 绘制描述框背景
        pygame.draw.rect(self.screen, (240, 240, 240), 
                         (desc_box_x, desc_box_y, self.DESC_BOX_WIDTH, desc_box_height))
        pygame.draw.rect(self.screen, (200, 200, 200), 
                         (desc_box_x, desc_box_y, self.DESC_BOX_WIDTH, desc_box_height), 2)
        
        # 绘制物品名称
        title_surf = font.render(item.replace('_', ' '), True, (0, 0, 0))
        self.screen.blit(title_surf, (desc_box_x + self.DESC_BOX_PADDING, desc_box_y + self.DESC_BOX_PADDING))
        
        # 绘制描述文本
        y_offset = desc_box_y + self.DESC_BOX_PADDING + line_height + 10
        for line in lines:
            line_surf = font.render(line, True, (50, 50, 50))
            self.screen.blit(line_surf, (desc_box_x + self.DESC_BOX_PADDING, y_offset))
            y_offset += line_height + self.DESC_LINE_SPACING
    
    def open(self, inventory):
        """打开背包"""
        self.bag_is_open = True
        unique_items, item_counts = self._process_inventory(inventory)
        total_pages = max(1, (len(unique_items) + self.ITEMS_PER_PAGE - 1) // self.ITEMS_PER_PAGE)
        clock = pygame.time.Clock()
        
        while self.bag_is_open:
            # 绘制背景
            self.screen.blit(self.BG_IMAGE,(0,0))
            
            # 绘制背包内容
            self._draw_grid(unique_items, item_counts)
            self._draw_page_info(total_pages)
            
            # 获取鼠标位置并更新悬停状态
            mouse_pos = pygame.mouse.get_pos()
            self.hovered_item = None
            for i in range(self.ITEMS_PER_PAGE):
                index = self.current_page * self.ITEMS_PER_PAGE + i
                if index < len(unique_items):
                    item = unique_items[index]
                    col = i % self.GRID_COLS
                    row = i // self.GRID_COLS
                    x = self.GRID_START_X + col * (self.GRID_CELL_SIZE + self.GRID_SPACING)
                    y = self.GRID_START_Y + row * (self.GRID_CELL_SIZE + self.GRID_SPACING)
                    item_rect = pygame.Rect(x, y, self.GRID_CELL_SIZE, self.GRID_CELL_SIZE)
                    if item_rect.collidepoint(mouse_pos):
                        self.hovered_item = item
                        break
            
            # 事件处理 (保持原有代码不变)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.bag_is_open = False
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_b:
                        self.bag_is_open = False
                    elif event.key == pygame.K_LEFT and self.current_page > 0:
                        self.current_page -= 1
                    elif event.key == pygame.K_RIGHT and self.current_page < total_pages-1:
                        self.current_page += 1

            if self.hovered_item:
                self._draw_description(self.hovered_item)
            
            pygame.display.update()
            clock.tick(60)
        
        return True