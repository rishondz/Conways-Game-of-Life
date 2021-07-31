class Button:
    def __init__(self, text, x, y, color = "lightblue", color2 = "green"):
        self.x, self.y = x, y
        self.text = FONT.render(text, 1, pygame.Color("Black"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.rect = pygame.Rect(x, y, self.size[0], self.size[1])
        self.color = pygame.Color(color)
        self.color2 = color2
        self.surface.fill(self.color)
    def select(self, x, y):
        if self.rect.collidepoint(x, y):
            self.color = self.color2
            self.surface.fill(self.color2)
            return True;
    def show(self):
        WIN.blit(self.surface, (self.x, self.y))
        WIN.blit(self.text, (self.x, self.y))
class Start_Button(Button):
    def select(self, x, y):
        if self.rect.collidepoint(x, y):
            temp = self.color
            self.color = self.color2
            self.color2 = temp
            self.surface.fill(self.color2)
            return True;