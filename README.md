# mcpi-block-structure
Small utility package built on mcpi to enable loading and saving of large cuboids in MineCraft.  If you have cuboids greater than 32768 blocks to store/load in Minecraft, this is an alternative that takes some time to store, but lets you store huge cuboids.<br><br>

<b>Installation</b><br>
To include this package in your codebase, clone it to the folder (or as a submodule to an existing repo) where you have python code that will run against an mcpi instance.

<b>Example</b><br>
```python
  from mcpi.minecraft import Minecraft
  from mcpi import vec3
  from mcpi_block_structure.blockstructure import BlockStructure
  
  mc = Minecraft.create('xxx.xxx.xxx.xxx',yyyy)  # where x is the ip for your MineCraft server running Raspberry Juice plugin and mcpi
  
  my_cuboid = BlockStructure(mc)
  NW_bottom_corner = my_cuboid.get_mcpi_vec_from_world_coords(39522, 78, 39968)
  SE_top_corner = my_cuboid.get_mcpi_vec_from_world_coords(39538, 88, 39977)
  my_cuboid.get_structure(start_pos_vec3=NW_bottom_corner, end_pos_vec3=SE_top_corner)  # stores the cuboid in memory accessible as my_cuboid.structure
  
  
  my_cuboid.write_to_file("my_cuboid.pkl") # stores as pickle file
  
  
  my_other_cuboid = BlockStructure(mc)
  other_NW_bottom_corner = my_other_cuboid.get_mcpi_vec_from_world_coords(39554,12,39826)
  my_other_cuboid.read_from_file("my_cuboid.pkl")
  my_other_cuboid.set_structure(other_NW_bottom_corner)
  
'''

