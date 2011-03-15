//
//  TimelineViewController.m
//  classiwhale
//
//  Created by Emilio Lopez on 3/14/11.
//  Copyright 2011 Stanford. All rights reserved.
//

#import "TimelineViewController.h"
#import "ClassiwhaleSingleton.h"
#import "TimelineCell.h"

@implementation TimelineViewController

@synthesize table;
@synthesize segmentedControl;
@synthesize userID;

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView {
	// Return the number of sections.
	return 1;
}


// Implement viewDidLoad to do additional setup after loading the view, typically from a nib.
- (void)viewDidLoad {
    [super viewDidLoad];
  ClassiwhaleSingleton *api = [ClassiwhaleSingleton sharedInstance];
	[[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(gotTwitterPic:) name:@"Got Twitter Pic" object:api];

	table.rowHeight = 82;
  NSURLResponse *response = nil;
  NSError *error = nil;

	timeline = ((!userID || [userID isEqualToString:@""]) ?
							[[api getFilteredTimelineWithResponse:&response andError:&error] objectForKey:@"statuses"] :
							[[api getFriendTimeline:userID withResponse:&response andError:&error] objectForKey:@"statuses"]);
	[timeline retain];
  [table reloadData];  
  //[api rateTweetId:@"47581699944615936" up:NO withResponse:&response andError:&error];
}

- (IBAction)segmentSwitched {
	ClassiwhaleSingleton *api = [ClassiwhaleSingleton sharedInstance];
	NSURLResponse *response = nil;
  NSError *error = nil;
  if (segmentedControl.selectedSegmentIndex == 0) {
		timeline = [[api getFilteredTimelineWithResponse:&response andError:&error] objectForKey:@"statuses"] ;
  }
  else{
		timeline = [[api getTimelineWithResponse:&response andError:&error] objectForKey:@"statuses"] ;
	}
	[timeline retain];
	[table reloadData];
}

- (IBAction) likeClicked:(id)sender
{
	TimelineCell *cell = (TimelineCell *)[[sender superview] superview];
	NSIndexPath *indexPath = [table indexPathForCell:cell];
	[cell.dislikeButton setImage:[UIImage imageNamed:@"dislike_btn.png"] forState:UIControlStateNormal];
	[cell.likeButton setImage:[UIImage imageNamed:@"like_btn_selected.png"] forState:UIControlStateNormal];
  NSString *tweetID = [[[timeline objectAtIndex:indexPath.row] valueForKey:@"id"] stringValue];
	[self submitRating:YES tweetID:tweetID];
}


- (IBAction) dislikeClicked:(id)sender
{
	TimelineCell *cell = (TimelineCell *)[[sender superview] superview];
	NSIndexPath *indexPath = [table indexPathForCell:cell];
	[cell.likeButton setImage:[UIImage imageNamed:@"like_btn.png"] forState:UIControlStateNormal];
	[cell.dislikeButton setImage:[UIImage imageNamed:@"dislike_btn_selected.png"] forState:UIControlStateNormal];
  NSString *tweetID = [[[timeline objectAtIndex:indexPath.row] valueForKey:@"id"] stringValue];
	[self submitRating:NO tweetID:tweetID];
}

- (void) submitRating:(Boolean)rating tweetID:(NSString*)tweetID
{
	NSURLResponse *response = nil;
  NSError *error = nil;
	NSLog(@"Tweet ID: %@", tweetID); 
	[[ClassiwhaleSingleton sharedInstance] rateTweetId:tweetID up:rating withResponse:&response andError:&error];
}

- (void)gotTwitterPic:(NSNotification *)info {
	NSDictionary *twitterPic = [info userInfo];
	for (NSDictionary *status in timeline) {
		if ([[twitterPic valueForKey:@"id"] isEqual:[[status objectForKey:@"_user_cache"] valueForKey:@"profile_image_url"]]) {
			NSUInteger cur_index = [timeline indexOfObject:status];
			[status setValue:[UIImage imageWithData:[twitterPic valueForKey:@"data"]] forKey:@"fetched_image"];
			NSUInteger indexes [] = {0, cur_index};
			[self.table reloadRowsAtIndexPaths:[NSArray arrayWithObject:[NSIndexPath indexPathWithIndexes:indexes length:2]] withRowAnimation:UITableViewRowAnimationNone];
		}
	}
}

- (NSInteger) tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
	// Return the number of rows in the section.
	return (timeline != nil ? [timeline count] : 0);
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
	static NSString *CellIdentifier = @"TimelineCell";
	
	TimelineCell *cell = (TimelineCell*)[tableView dequeueReusableCellWithIdentifier:CellIdentifier];
	if (cell == nil) {
		NSArray *topLevelObjects = [[NSBundle mainBundle] loadNibNamed:@"TimelineCell"
																														 owner:nil options:nil];
		for (id currentObject in topLevelObjects) {
			if ([currentObject isKindOfClass:[UITableViewCell class]]) {
				cell = (TimelineCell*)currentObject;
				break;
			}
		}
	}
	if ([timeline count] > indexPath.row) {
		NSDictionary *status = [timeline objectAtIndex:indexPath.row];
		NSLog(@"%@", status);
		
		UILabel *myLabel = [[[UILabel alloc] initWithFrame:CGRectMake(50.0,50.0,245.0,150.0)] autorelease];
		myLabel.numberOfLines = 0;
		myLabel.lineBreakMode = UILineBreakModeWordWrap;
		myLabel.text = [status valueForKey:@"text"];
		myLabel.font = [UIFont fontWithName:@"Helvetica" size:13];
		CGSize labelSize = [myLabel.text sizeWithFont:myLabel.font constrainedToSize:myLabel.frame.size lineBreakMode:UILineBreakModeWordWrap];
		cell.tweet.frame = CGRectMake(cell.tweet.frame.origin.x, cell.tweet.frame.origin.y, labelSize.width, labelSize.height);

		cell.tweet.text = [status valueForKey:@"text"];
		cell.username.text = [[status objectForKey:@"_user_cache"] valueForKey:@"screen_name"];
		cell.date.text = [status valueForKey:@"created_at"];
		
		[cell.likeButton setImage:[UIImage imageNamed:@"like_btn.png"] forState:UIControlStateNormal];
		[cell.dislikeButton setImage:[UIImage imageNamed:@"dislike_btn.png"] forState:UIControlStateNormal];
		if ([status valueForKey:@"rating"]) {
			if ([[status valueForKey:@"rating"] intValue] == 1)
				[cell.likeButton setImage:[UIImage imageNamed:@"like_btn_selected.png"] forState:UIControlStateNormal];
			else 
				[cell.dislikeButton setImage:[UIImage imageNamed:@"dislike_btn_selected.png"] forState:UIControlStateNormal];
		}
		if ([status valueForKey:@"fetched_image"]) {
			[[cell act] stopAnimating];
			cell.profileImage.image = [status valueForKey:@"fetched_image"];
		} else {
			cell.profileImage.image = nil;
			[[ClassiwhaleSingleton sharedInstance] fetchProfilePic:[[status objectForKey:@"_user_cache"] valueForKey:@"profile_image_url"]];
		};
		
	}
	return cell;
}

- (CGFloat)tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath {
	
	UILabel *myLabel = [[[UILabel alloc] initWithFrame:CGRectMake(50.0,50.0,245.0,150.0)] autorelease];
	myLabel.numberOfLines = 0;
	myLabel.lineBreakMode = UILineBreakModeWordWrap;
	myLabel.text = [[timeline objectAtIndex:indexPath.row] valueForKey:@"text"];
	myLabel.font = [UIFont fontWithName:@"Helvetica" size:13];
	CGSize labelSize = [myLabel.text sizeWithFont:myLabel.font constrainedToSize:myLabel.frame.size lineBreakMode:UILineBreakModeWordWrap];
	return labelSize.height+61;
	
}


- (void)didReceiveMemoryWarning {
    // Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
    
    // Release any cached data, images, etc. that aren't in use.
}

- (void)viewDidUnload {
    [super viewDidUnload];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}


- (void)dealloc {
    [super dealloc];
}


@end
