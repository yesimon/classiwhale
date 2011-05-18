//
//  SearchViewController.m
//  classiwhale
//
//  Created by Emilio Lopez on 3/14/11.
//  Copyright 2011 Stanford. All rights reserved.
//

#import "SearchViewController.h"
#import "ClassiwhaleSingleton.h"
#import "TimelineCell.h"

@implementation SearchViewController

- (void)viewDidLoad {
	[super viewDidLoad];
}

- (NSInteger)numberOfSectionsInTableView:(UITableView *)aTableView {
	return (_data != nil ? [_data count] : 0);
}

- (NSInteger)tableView:(UITableView *)aTableView numberOfRowsInSection:(NSInteger)section {
	return [_data count];
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
	if ([_data count] > indexPath.row) {
		NSDictionary *status = [_data objectAtIndex:indexPath.row];
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

- (void)searchClassiwhale:(NSString*)query
{
	[_data removeAllObjects];
	[_data release];
	ClassiwhaleSingleton *api = [ClassiwhaleSingleton sharedInstance];
	NSURLResponse *response = nil;
  NSError *error = nil;
	_data = [[[api getSearchWithResponse:&response andError:&error andQuery:query] 
						objectForKey:@"statuses"] retain] ;
}

- (BOOL)searchDisplayController:(UISearchDisplayController *)controller shouldReloadTableForSearchString:(NSString *)searchString
{
	[self searchClassiwhale:searchString];
	return YES;
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
