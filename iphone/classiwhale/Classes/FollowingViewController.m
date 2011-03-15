//
//  FollowingViewController.m
//  classiwhale
//
//  Created by Emilio Lopez on 3/14/11.
//  Copyright 2011 Stanford. All rights reserved.
//

#import "FollowingViewController.h"
#import "TwitterUserCell.h"
#import "ClassiwhaleSingleton.h"
#import "TimelineViewController.h"


@implementation FollowingViewController

@synthesize table;


- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView {
	// Return the number of sections.
	return 1;
}



- (void)gotTwitterPic:(NSNotification *)info {
	NSDictionary *twitterPic = [info userInfo];
	for (NSDictionary *user in users) {
		if ([[twitterPic valueForKey:@"id"] isEqual:[user valueForKey:@"profile_image_url"]]) {
			NSUInteger cur_index = [users indexOfObject:user];
			[user setValue:[UIImage imageWithData:[twitterPic valueForKey:@"data"]] forKey:@"fetched_image"];
			NSUInteger indexes [] = {0, cur_index};
			[self.table reloadRowsAtIndexPaths:[NSArray arrayWithObject:[NSIndexPath indexPathWithIndexes:indexes length:2]] withRowAnimation:UITableViewRowAnimationNone];
		}
	}
}


- (NSInteger) tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
	// Return the number of rows in the section.
	return (users != nil ? [users count] : 0);
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
	static NSString *CellIdentifier = @"TwitterUserCell";
	
	TwitterUserCell *cell = (TwitterUserCell*)[tableView dequeueReusableCellWithIdentifier:CellIdentifier];
	if (cell == nil) {
		NSArray *topLevelObjects = [[NSBundle mainBundle] loadNibNamed:CellIdentifier
																														 owner:nil options:nil];
		for (id currentObject in topLevelObjects) {
			if ([currentObject isKindOfClass:[UITableViewCell class]]) {
				cell = (TwitterUserCell*)currentObject;
				break;
			}
		}
	}
	if ([users count] > indexPath.row) {
    
		NSDictionary *user = [users objectAtIndex:indexPath.row];
    
		cell.user_name.text = [user valueForKey:@"name"];
		cell.screen_name.text = [user valueForKey:@"screen_name"];
    
		if ([user valueForKey:@"fetched_image"]) {
      NSLog(@"%@", [cell act]);
      NSLog(@"%@", cell.profileImage);
			[[cell act] stopAnimating];
			cell.profileImage.image = [user valueForKey:@"fetched_image"];
		} else {
      NSLog(@"%@", user);
			cell.profileImage.image = nil;
			[[ClassiwhaleSingleton sharedInstance] fetchProfilePic:[user valueForKey:@"profile_image_url"]];
		};
		
	}
	return cell;
}

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
	TimelineViewController* userTimelineVC = [[[TimelineViewController alloc] 
																						 initWithNibName:@"UserTimelineViewController" bundle:[NSBundle mainBundle]] autorelease];
	NSDictionary* user = [users objectAtIndex:indexPath.row];
	userTimelineVC.title = [user valueForKey:@"screen_name"];
	userTimelineVC.userID = [[user valueForKey:@"id"] stringValue];
	[self.navigationController pushViewController:userTimelineVC animated:YES];
}


// The designated initializer.  Override if you create the controller programmatically and want to perform customization that is not appropriate for viewDidLoad.
/*
- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil {
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization.
    }
    return self;
}
*/


// Implement viewDidLoad to do additional setup after loading the view, typically from a nib.
 - (void)viewDidLoad {
  [super viewDidLoad];
  ClassiwhaleSingleton *api = [ClassiwhaleSingleton sharedInstance];
  [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(gotTwitterPic:) name:@"Got Twitter Pic" object:api];
 
  table.rowHeight = 73;
  NSURLResponse *response = nil;
  NSError *error = nil;
 
   users = [[api getFriendsWithResponse:&response andError:&error] valueForKey:@"friends"];
  [users retain];
  [table reloadData];
 }


/*
// Override to allow orientations other than the default portrait orientation.
- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation {
    // Return YES for supported orientations.
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}
*/

- (void)didReceiveMemoryWarning {
    // Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
    
    // Release any cached data, images, etc. that aren't in use.
}

- (void)viewDidUnload {
  [users release];
    [super viewDidUnload];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}


- (void)dealloc {
    [super dealloc];
}


@end
