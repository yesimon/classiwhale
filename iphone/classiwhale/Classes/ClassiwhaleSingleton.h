//
//  ClassiwhaleSingleton.h
//  classiwhale
//
//  Created by Emilio Lopez on 3/14/11.
//  Copyright 2011 Stanford. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "SA_OAuthTwitterEngine.h" 
#import "SA_OAuthTwitterController.h"



@interface ClassiwhaleSingleton : NSObject <SA_OAuthTwitterControllerDelegate> {
	SA_OAuthTwitterEngine *twitterEngine;

  NSArray *cookies;
  BOOL authenticated;
	CFMutableDictionaryRef connections;
}

+ (ClassiwhaleSingleton*)sharedInstance;
- (void) loginToTwitter:(UIViewController*)vc;
- (NSDictionary *) getFilteredTimelineWithResponse:(NSURLResponse **)response andError:(NSError **)error;
- (NSDictionary *) getTimelineWithResponse:(NSURLResponse **)response andError:(NSError **)error;
- (NSArray *) getFriendsWithResponse:(NSURLResponse **)response andError:(NSError **)error;
- (NSArray *) rateTweetId:(NSString *)tweet_id up:(BOOL)rate_up withResponse:(NSURLResponse **)response andError:(NSError **)error;
- (NSArray *) getFriendTimeline:(NSString *)friend_id withResponse:(NSURLResponse **)response andError:(NSError **)error;
- (void) fetchProfilePic:(NSString*) urlString;
- (void) createConnection:(NSURL*)url postBody:(NSData*)postBody method:(NSString*)method cid:(NSString*)cid;
- (void) authenticatedWithCookies: (NSArray *) cooks;
- (void) preapprovedWithCookies: (NSArray *) cooks;

@property (nonatomic, retain) NSArray *cookies;
@property BOOL authenticated;

@end
