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
}

+ (ClassiwhaleSingleton*)sharedInstance;
- (void) loginToTwitter:(UIViewController*)vc;
- (NSArray *) getFilteredTimelineWithResponse:(NSURLResponse **)response andError:(NSError **)error;
- (NSArray *) getTimelineWithResponse:(NSURLResponse **)response andError:(NSError **)error;

@property (nonatomic, retain) NSArray *cookies;
@property BOOL authenticated;

@end
