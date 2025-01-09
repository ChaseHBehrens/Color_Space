# Color Space
These programs were designed to generate color palettes by evenly dividing the color spectrum. The goal is to decrease color count needed for games while retaining coverage over the entire color spectrum. 
# How to use
color13 and on use arrow keys to rotate the 3d environment.
# Initial versions
I started by creating an even distribution over the RGB color space. However this is not perceived uniformly by the human eye. There are visually distinct sections of smoothness and separation around the edges.
<br><br>
![image](https://github.com/user-attachments/assets/9d64204b-de6f-4de4-a8f0-dd7f8dffa543)
# CIELAB color space
With more research I discovered the CIELAB color space which groups color based on human perception. It groups color based on hue, chroma, and brightness.
![image](https://github.com/user-attachments/assets/007762f4-e44f-40d3-87a3-39f5e0e01880)
# 3D representation
My best versions so far have been by dividing the CIELAB color space using a hexagonal lattice and a fibonacci lattice.
<br><br>
![image](https://github.com/user-attachments/assets/7c85abb1-9807-4a68-bd01-61ac096d39d5)
![image](https://github.com/user-attachments/assets/285a2ee0-91b8-406e-8566-961bbe5f6662)
![image](https://github.com/user-attachments/assets/3890f6d8-367c-41c0-8925-831245f65caa)

# Future plans
I would like a version that both evenly divides the color spectrum but also provides smooth gradients in multiple directions for better use in art. Ultimately, I want to develop a hash function that can palletize any color in constant time. This would allow for features like algorithmic colored lighting in games. 
