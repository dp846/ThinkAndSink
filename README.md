# Think And Sink

This is a game based on the popular boardgame Battleships! It includes:
 - a regular Battleships game mode for 2 players
 - a regular Battleships game mode for 1 player against a very good AI opponent using Monte Carlo simulation techniques
 - a custom made, 1 player game mode where the ships move around the board, where the aim is to sink them in as few moves, and as quickly as possible
 - and an original game soundtrack for an old video game feel composed by me
  
## Battleships vs AI opponent

The player makes guesses on the grid on the left, and the AI responds with its guess on the right hand grid.
- Grey means a miss
- Red means a hit
- Purple means an entire sunk ship  

A text display in the centre will output the events of a game - sunk ships, the winner, and the number of turns taken to win.

![image](https://user-images.githubusercontent.com/117474143/224710343-4d60d513-f711-4f89-ab7c-d8e8656b5b8d.png)

When the game is finished, the remaining ship positions are highlighted: 

![image](https://user-images.githubusercontent.com/117474143/224711697-e4aa12e7-3899-4bdf-88f0-0b3d22f54909.png)  


## The custom game mode is called Chaos Mode

![image](https://user-images.githubusercontent.com/117474143/224709072-51714f2a-ce6d-42fb-8524-cda21671754c.png)

These are the rules of CHAOS MODE!  
=> You play against the computer for the least number of turns to destroy all 7 ships on a large grid.  
=> 7 ships will spawn in random positions facing in random directions, with their positions unknown to the player.   
=> There's a twist - the ships will move in the direction they are facing every turn you take, so you had better pay attention to where they are going.  
=> Upon reaching an edge, or another ship, the ships will rotate 180 degrees and travel back in the opposite direction.  
=> It is your job to destroy every ship in as few turns as possible or in the quickest time.   
=> As it is a large grid, guessing is no longer a singular coordinate, it gets more interesting.  
=> Your turn consists of different options. You can use:  
====> 'Bombing run' - launch an aerial strike on the grid hitting all the co-ordinates on a single row or column of your choice.  
====> 'Missile' - launch a missile that hits a very large circular area on the grid damaging any ships it hits.   
====> 'Torpedo' - launch a torpedo that hits a medium-sized square area on the grid damaging any ships it hits.   
====> 'Focussing laser' - confident on where a ship is? This attack will hit a direct concentrated cross area for high damage. Risk for reward. 
====> 'Scattershot' - strategically choose 10 specific co-ordinates to attack dealing damage to any ships hit. Or, you know, you could just spam random co-ordinates...  
====> 'Sonar' - if you're not sure where to attack or simply want information, the sonar tool takes a turn to display of where the front co-ordinate of each ship on the grid was on the PREVIOUS TURN. A useful tool, but it won't tell you where they are on the next turn!   
====> 'Freeze' - freezes the ocean, keeping the ships stationary for the next 2 turns (it must be very cold...)
=> Use these powerful attacks and strategic placements to get the least number of turns to destroy the ships, or aim for as fast a time as possible to sink them all.   
=> You cannot use an attack you used in your last 2 turns, so it's all about choosing the best option!   
=> Each ship has hitpoints (corresponding to its size, i.e, the larger the ship, the more hitpoints), and when its hitpoints drop to or below 0, BOOM! It sinks.  
=> Don't tunnel vision on just 1 ship at any one time, since remember - the others will be moving! The last thing anyone wants is a lost ship.   
=> Do not worry, you do not have to remember each ship's hitpoints! These are displayed to you so use this to your advantage on which to finish off or track down.   
=> A battle log on the screen will show messages based on the occurances of the match - whenever you sink or damage a ship, it tells you.   
=> Be sure to try different strategies each time you play. The sonar and missile combo might be more to your liking, or maybe using the freeze and then following up with a focussing laser on a ship is what you find best.   
=> Less turns means a better, and so a more efficient win.    
=> You can check the leaderboards to see who to knock off the top spot.    
  
![image](https://user-images.githubusercontent.com/117474143/224713645-fab40b4b-6b0b-430c-872d-4dc718f2f4f7.png)   

### Leaderboard

There is a leaderboard for Chaos Mode, which can be sorted by time or the number of turns, creating 2 ways to play - slow and strategic, or fast and chaotic

![image](https://user-images.githubusercontent.com/117474143/224714204-0389dfbc-da23-4dd7-b2b1-dc0216667a16.png)

### Statistics

You can see the outcomes of recent games, and additional information:  

![image](https://user-images.githubusercontent.com/117474143/224714347-c7137302-b464-4096-80ad-81b865bbe361.png)  

To play, simply navigate to the 'executable' folder and run ThinkAndSink.exe  

Created by Dan Parsley for an A* graded A-level Computer Science programming project.
