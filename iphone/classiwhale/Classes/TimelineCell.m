//
//  TimelineCell.m
//  classiwhale
//
//  Created by Emilio Lopez on 3/14/11.
//  Copyright 2011 Stanford. All rights reserved.
//

#import "TimelineCell.h"


@implementation TimelineCell

@synthesize username;
@synthesize tweet;
@synthesize date;
@synthesize profileImage;
@synthesize act;
@synthesize likeButton;
@synthesize dislikeButton;

- (id)initWithStyle:(UITableViewCellStyle)style reuseIdentifier:(NSString *)reuseIdentifier {
    
    self = [super initWithStyle:style reuseIdentifier:reuseIdentifier];
    if (self) {
        // Initialization code.
    }
    return self;
}


- (void)setSelected:(BOOL)selected animated:(BOOL)animated {
    
    [super setSelected:selected animated:animated];
    
    // Configure the view for the selected state.
}


- (void)dealloc {
    [super dealloc];
}


@end
