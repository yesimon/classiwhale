//
//  classiwhaleAppDelegate.m
//  classiwhale
//
//  Created by Emilio Lopez on 3/14/11.
//  Copyright 2011 Stanford. All rights reserved.
//

#import "classiwhaleAppDelegate.h"
#import "SplashScreenViewController.h"
#import "TimelineViewController.h"
#import "WhaleViewController.h"
#import "SearchViewController.h"
#import "FollowingViewController.h"

@implementation classiwhaleAppDelegate

@synthesize window;


#pragma mark -
#pragma mark Application lifecycle

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {    
    
	SplashScreenViewController *splash = [[SplashScreenViewController alloc] init];
	UINavigationController *nav = [[[UINavigationController alloc] init] autorelease];
	[nav pushViewController:splash animated:NO];
	nav.navigationBar.hidden = YES;
	[self.window addSubview:nav.view];
	[self.window makeKeyAndVisible];     
    
	return YES;
}

- (void) successfullyLoggedIn
{
	TimelineViewController *timelineVC = [[[TimelineViewController alloc] init] autorelease]; 
	timelineVC.title = @"Timeline";
	FollowingViewController *followingVC = [[[FollowingViewController alloc] init] autorelease]; 
	followingVC.title = @"Following";
	SearchViewController *searchVC = [[[SearchViewController alloc] init] autorelease]; 
	searchVC.title = @"Search";
	WhaleViewController *whaleVC = [[[WhaleViewController alloc] init] autorelease]; 
	whaleVC.title = @"My Whale";
	
	UINavigationController *timelineNav = [[[UINavigationController alloc] init] autorelease];
	timelineNav.tabBarItem.image = [UIImage imageNamed:@"newspaper.png"];
	UINavigationController *followingNav = [[[UINavigationController alloc] init] autorelease];
	followingNav.tabBarItem.image = [UIImage imageNamed:@"group.png"];
	UINavigationController *searchNav = [[[UINavigationController alloc] init] autorelease];
	searchNav.tabBarItem.image = [UIImage imageNamed:@"magnify.png"];
	UINavigationController *whaleNav = [[[UINavigationController alloc] init] autorelease];
	//whaleNav.tabBarItem.image = [UIImage imageNamed:@"tabbar_whale.png"];
	timelineNav.navigationBar.tintColor = [UIColor colorWithRed:51/255.0 green:51/255.0 blue:51/255.0 alpha:1.0]; 
	followingNav.navigationBar.tintColor = [UIColor colorWithRed:51/255.0 green:51/255.0 blue:51/255.0 alpha:1.0];  
	searchNav.navigationBar.tintColor = [UIColor colorWithRed:51/255.0 green:51/255.0 blue:51/255.0 alpha:1.0]; 
	whaleNav.navigationBar.tintColor = [UIColor colorWithRed:51/255.0 green:51/255.0 blue:51/255.0 alpha:1.0];  
	
	[timelineNav pushViewController:timelineVC animated:NO];
	[followingNav pushViewController:followingVC animated:NO];
	[searchNav pushViewController:searchVC animated:NO];
	[whaleNav pushViewController:whaleVC animated:NO];
	
	UITabBarController* tabBarController = [[UITabBarController alloc] init]; 
	tabBarController.viewControllers = [NSArray arrayWithObjects: timelineNav, followingNav, searchNav, whaleNav, nil]; 
	
	
	// Add the tab bar controller's view to the window and display.
	[self.window addSubview:tabBarController.view];
	[self.window makeKeyAndVisible];	
}


- (void)applicationWillResignActive:(UIApplication *)application {
    /*
     Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
     Use this method to pause ongoing tasks, disable timers, and throttle down OpenGL ES frame rates. Games should use this method to pause the game.
     */
}


- (void)applicationDidEnterBackground:(UIApplication *)application {
    /*
     Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later. 
     If your application supports background execution, called instead of applicationWillTerminate: when the user quits.
     */
}


- (void)applicationWillEnterForeground:(UIApplication *)application {
    /*
     Called as part of  transition from the background to the inactive state: here you can undo many of the changes made on entering the background.
     */
}


- (void)applicationDidBecomeActive:(UIApplication *)application {
    /*
     Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
     */
}


- (void)applicationWillTerminate:(UIApplication *)application {
    /*
     Called when the application is about to terminate.
     See also applicationDidEnterBackground:.
     */
}


#pragma mark -
#pragma mark Memory management

- (void)applicationDidReceiveMemoryWarning:(UIApplication *)application {
    /*
     Free up as much memory as possible by purging cached data objects that can be recreated (or reloaded from disk) later.
     */
}


- (void)dealloc {
    [window release];
    [super dealloc];
}


@end
