# MDRL
A minimal HTTP Discord API wrapper intended for self-botting

    This is a work in progress, and will likely introduce breaking changes.
    
# How to install

    pip install git+https://github.com/ralphrimwell/MDRL.git

## Todo

  

    - Ratelimit handler, possibly seperate from the client to account for ip instead of user
    
    - Headers generator, to allow for more random data
    
    - Guild permissions calculator (NOTE: probably should be avoided as you have to do so many requests (resulting in rate limiting) to get the required information, on connection to the websocket it returns basically all the information needed, so will probably only be implemented if websocket is implemented)
