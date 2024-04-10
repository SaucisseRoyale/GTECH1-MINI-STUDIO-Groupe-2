        self.rect.x += dx
        self.rect.y += dy

        # Nouvelle gestion des collisions avec les tuiles en utilisant les masques
        for tile in world.tile_list:
            # Obtention de la position relative du joueur par rapport à la tuile pour la vérification des masques
            offset_x = tile[1].x - self.rect.x
            offset_y = tile[1].y - self.rect.y
            
            # Vérification de la collision entre le masque du joueur et celui de la tuile
            collision_point = self.mask.overlap(tile[3], (offset_x, offset_y))
            
            if collision_point:
                # Collision détectée, gérer en fonction de la position et du type de collision
                if dy > 0:  
                    self.rect.y = tile[1].y - self.height
                    dy = 0
                    self.on_ground = True
                    self.vel_y = 0
                elif dy < 0:
                    self.rect.y = tile[1].bottom
                    dy = 0
                    self.vel_y = 0
                if dx > 0:  
                    self.rect.x = tile[1].left - self.width
                    dx = 0
                elif dx < 0:
                    self.rect.x = tile[1].right
                    dx = 0