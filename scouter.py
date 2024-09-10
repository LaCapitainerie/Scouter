'''
//////////////////////////////////////
||||||||||||||||||||||||||||||||||||||

   ******   ****     **  *******   ******* 
  **////** /**/**   /** /**////** /**////**
 **    //  /**//**  /** /**   /** /**   /**
/**        /** //** /** /*******  /******* 
/**        /**  //**/** /**////   /**////  
//**    ** /**   //**** /**       /**      
 //******  /**    //*** /**       /**      
  //////   //      ///  //        //   
  
||||||||||||||||||||||||||||||||||||||
//////////////////////////////////////
'''



from Assets.Assets import *
from Client.Clients import *
from Technos.Technos import *
from Global.Login import Login
from Perimeters.Perimeters import *
from Pipeline.Pipeline import Mode, Pipeline
from Global.Sync import get_data



def main():

    from pandas import read_csv
    Devices = read_csv("devices 1.csv", sep=";")
    del read_csv

    Loop = Devices[Devices.Domain.isin(["cnpp.fr"])]["Device Name"].iloc[:10].values

    Pipeline(

        Mode.PLAN,
        True,
        
        Login,
        get_data,

        (get_client, {"name": "CNPP"}),

        (add_perimeter, {"client": "CNPP", "name": "Device Param"}),

        (add_mass_assets, {"column": Loop}),


        file="const.json"

    ).run()

    """
    (add_perimeter, {"client": "CNPP", "name": "Test Perimetre"}),
    delete_perimeter,
    delete_perimeter,
    add_perimeter,


    (add_asset, {"name": "test2", "description": "test"}),
    delete_asset,
    delete_asset,
    add_asset,


    (add_techno, {"name": "Techno test", "description": "test", "vendor": "test", "version": "test"}),
    delete_techno,
    delete_techno,
    add_techno,
    """

if __name__ == '__main__':
    main()