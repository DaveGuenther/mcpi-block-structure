from mcpi.minecraft import Minecraft
from mcpi import vec3
from mcpi import block
import pickle
import math

class BlockStructure:
    structure=[]
    
    def __init__(self, mcpi_connection):
        self.mc_connection = mcpi_connection
    
    def get_world_coords_from_mcpi_vec(self, this_vec):
        this_vec.x-=32
        this_vec.y+=66
        this_vec.z+=128
        return vec3.Vec3(x,y,z)    
    
    def get_mcpi_vec_from_world_coords(self, x, y, z):
        x+=32
        y-=66
        z-=128
        return vec3.Vec3(x,y,z)    
    
    def get_mcpi_vec_from_world_vec(self, this_vec):
        this_vec.x+=32
        this_vec.y-=66
        this_vec.z-=128
        return this_vec 
    
    def get_structure(self, start_pos_vec3, end_pos_vec3):
        """
        start_vec3: Vec3 representation of an x,y,z coordinate of one corner of the cuboid to save.  This object is located at mcpi.vec3.Vec3(x, y, z)
                    The start_pos_vec3 vector must be at the base of the structure on the NW corner.  If you stand at the corner of the structure and
                    look away from it, and find that you are facing just between north and west, you're on the right corner.
        end_vec3:   Vec3 representation of an x,y,z coordinate of the opposite corner of the cuboid to save.  This object is located at mcpi.vec3.Vec3(x, y, z)

                    The end_pos_vec3 vector must be at the top of the structure on the SE corner.
        """
        
        x_dist = end_pos_vec3.x+1-start_pos_vec3.x
        y_dist = end_pos_vec3.y+1-start_pos_vec3.y
        z_dist = end_pos_vec3.z+1-start_pos_vec3.z
        total_blocks = x_dist*y_dist*z_dist
        print('Total Blocks to store:',total_blocks)
        input("Press a key to start")
        current_block=0
        structure_data =[]
        for y,world_y in zip(range (y_dist),range (start_pos_vec3.y, end_pos_vec3.y+1)):
            for x,world_x in zip(range (x_dist),range (start_pos_vec3.x, end_pos_vec3.x+1)):
                for z,world_z in zip(range (z_dist),range (start_pos_vec3.z, end_pos_vec3.z+1)):
                    #print(str(round((current_block/total_blocks)*100,2))+"%"+"  |  x: "+str(x)+"   y: "+str(y)+"   z: "+str(z)+"   Block: "+str(mc.getBlockWithData(x,y,z)))
                    #print(str(round((current_block/total_blocks)*100,2))+"%"+"  |  w_x: "+str(world_x)+"   w_y: "+str(world_y)+"   w_z: "+str(world_z)+"   Block: "+str(mc.getBlockWithData(x,y,z)))
                    this_vector = vec3.Vec3(x,y,z)
                    block_data=self.mc_connection.getBlockWithData(world_x,world_y,world_z)
                    #print(str(round((current_block/total_blocks)*100,2))+"%"+"  |  Vector: "+"("+str(world_x)+", "+ str(world_y)+", " + str(world_z)+")   Block: "+str(block_data))
                    print(".",end='')
                    structure_data.append([this_vector.x, this_vector.y, this_vector.z, block_data])
                    current_block+=1
                    #print("x:",x,"  y:",y,"  z:",z,"  Block:",mc.getBlockWithData(x,y,z))
        #print('Total Blocks to store:',total_blocks)
        self.structure = structure_data

    
    def set_structure(self, bot_nw_corner, rotate_by_deg=0, rotation_center=vec3.Vec3(0,0,0), replace_air=True, erase_structure=False):
        """
        start_vec3:        Vec3 representation of an x,y,z coordinate of one corner of the cuboid to save.  This object is located at mcpi.vec3.Vec3(x, y, z)
                           The start_pos_vec3 vector must be at the base of the structure on the NW corner.  If you stand at the corner of the structure and
                           look away from it, and find that you are facing just between north and west, you're on the right corner.

        rotate_by_deg:     Value in degrees to rotate the structure around the origin.  Default is 0 degrees.

        rotation_center:   Central point to rotate structure around.  y coordinate shouldbe at bottom of model.

        replace_air:       Boolean value.  Some blocks in the model may contain air.  Set to true if you wish to replace whatever blocks
                           existed in the world before with air in those cases.  Set to false if you wish to skip over air blocks in the
                           model you are loading, leaving whatever existed in the world before hand to stay.

        erase_structure:   Boolean Value.  Set to True if you wish to place AIR blocks in every block position of the loaded model (essentially creating a
                           cuboid of air).  This effectively erases whatever was in that place before.  This is set to false by default.  Keep it set to false
                           if you wish to load a structure into the world.


        """
        structure_data = self.structure
        #print(structure_data)
        angle=rotate_by_deg*(math.pi/180)
        for this_block in structure_data:
            block_pos_x = this_block[0]
            block_pos_y = this_block[1]
            block_pos_z = this_block[2]
            block_data = this_block[3]
            #print(block_data)
            #print(block.Block(0,0))
            if rotate_by_deg!=0:
                block_pos_x, block_pos_z = rotate((rotation_center.x, rotation_center.z),(block_pos_x,block_pos_z),angle)

            this_pos_vec = vec3.Vec3(block_pos_x+bot_nw_corner.x, block_pos_y+bot_nw_corner.y, block_pos_z+bot_nw_corner.z)
            #print(this_pos_vec.x, this_pos_vec.y, this_pos_vec.z)
            if erase_structure:
                block_data=0
            if replace_air:
                self.mc_connection.setBlock(this_pos_vec.x, this_pos_vec.y, this_pos_vec.z, block_data)
            else:
                if block_data!=block.Block(0,0):
                    
                    self.mc_connection.setBlock(this_pos_vec.x, this_pos_vec.y, this_pos_vec.z, block_data)

    def write_to_file(self, filename):
        pickle.dump(self.structure,open( filename, "wb" ))
        
    def read_from_file(self, filename):
        self.structure = pickle.load(open( filename, "rb" ))