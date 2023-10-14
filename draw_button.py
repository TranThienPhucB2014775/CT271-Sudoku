import pygame
from path import Path

dir = Path()

pygame.font.init()
font = pygame.font.Font(dir.get_path() + '/fonts/OpenSans-Regular.ttf',25)

#vẽ đường viền và chữ vào
def Draw_button( button_ , screen, button_size, location, text, font_size, color_boder, color_text):
            #vẽ đường viền
            border_thickness = 2
            pygame.draw.rect(screen, color_boder , button_, border_thickness)
            #vẽ chữ
            result_text = font.render(text, True, color_text)
            #kích thướt của chữ
            text_rect = result_text.get_rect()
            screen.blit(result_text, (location[0] + (button_size[0] - text_rect.width)/ 2, location[1]  +  (button_size[1] - text_rect.height) / 2 ))