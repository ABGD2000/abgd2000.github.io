----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    22:38:45 03/10/2010 
-- Design Name: 
-- Module Name:    MUXb - Behavioral 
-- Project Name: 
-- Target Devices: 
-- Tool versions: 
-- Description: 
--
-- Dependencies: 
--
-- Revision: 
-- Revision 0.01 - File Created
-- Additional Comments: 
--
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

---- Uncomment the following library declaration if instantiating
---- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity MUX4 is
	generic (n: natural := 8);
    Port ( I0 : in  STD_LOGIC_VECTOR (n-1 downto 0);
           I1 : in  STD_LOGIC_VECTOR (n-1 downto 0);
           I2 : in  STD_LOGIC_VECTOR (n-1 downto 0);
           I3 : in  STD_LOGIC_VECTOR (n-1 downto 0);
           S : in  STD_LOGIC_Vector (1 downto 0) ;
           O : out STD_LOGIC_VECTOR (n-1 downto 0));
end MUX4;

architecture Behavioral of MUX4 is

begin

	O <= 	I0 when S = "00" else
			I1 when S = "01" else 
			I2 when S = "10" else 
			I3 when S = "11" ;
end Behavioral;

