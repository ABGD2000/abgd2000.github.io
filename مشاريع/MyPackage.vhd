--	Package File Template
--
--	Purpose: This package defines supplemental types, subtypes, 
--		 constants, and functions 


library IEEE;
use IEEE.STD_LOGIC_1164.all;

package MyPackage is

component MUX4 is
GENERIC(n:NATURAL);
    Port ( I0 : in  STD_LOGIC_VECTOR (n-1 downto 0);
           I1 : in  STD_LOGIC_VECTOR (n-1 downto 0);
           I2 : in  STD_LOGIC_VECTOR (n-1 downto 0);
           I3 : in  STD_LOGIC_VECTOR (n-1 downto 0);
           S : in  STD_LOGIC_Vector (1 downto 0) ;
           O : out STD_LOGIC_VECTOR (n-1 downto 0));
end component;
 
component Decoder4 is
    Port ( I : in  STD_LOGIC_VECTOR (1 downto 0);
           O : out  STD_LOGIC_VECTOR (3 downto 0);
           ena : in  STD_LOGIC);
end component;

component FullAdder is
    Port ( A : in  STD_LOGIC;
           B : in  STD_LOGIC;
           Cin : in  STD_LOGIC;
           S : out  STD_LOGIC;
           Cout : out  STD_LOGIC);
end component;


component AdderSubtractor4 is
    Port ( Input1 : in  STD_LOGIC_VECTOR (3 downto 0);
           Input2 : in  STD_LOGIC_VECTOR (3 downto 0);
           Mode : in  STD_LOGIC;
           Result : out  STD_LOGIC_VECTOR (3 downto 0));
end component;

end MyPackage;
