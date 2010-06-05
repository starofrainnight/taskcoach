//
//  TaskDetailsGeneral.m
//  TaskCoach
//
//  Created by Jérôme Laheurte on 16/05/10.
//  Copyright 2010 Jérôme Laheurte. All rights reserved.
//

#import "TaskCoachAppDelegate.h"

#import "TaskDetailsGeneral.h"
#import "TaskCategoryPickerController.h"

#import "CDTask.h"
#import "CDDomainObject+Addons.h"

#import "i18n.h"

@interface TaskDetailsGeneral ()

- (void)onSaveDescription:(UIBarButtonItem *)button;

@end;

@implementation TaskDetailsGeneral

@synthesize subject;
@synthesize descriptionLabel;
@synthesize description;
@synthesize categoriesButton;

- initWithTask:(CDTask *)theTask parent:(TaskDetailsController *)parent
{
	if (self = [super initWithNibName:@"TaskDetailsGeneral" bundle:[NSBundle mainBundle]])
	{
		task = [theTask retain];
		parentCtrl = parent;
	}

	return self;
}

- (void)viewDidLoad
{
	[super viewDidLoad];

	self.subject.text = task.name;
	self.description.text = task.longDescription;

	self.navigationItem.title = task.name;

	self.descriptionLabel.text = _("Description");
	self.categoriesButton.titleLabel.text = _("Categories");

	if (![task.name length])
		[subject becomeFirstResponder];
}

- (void)viewDidUnload
{
	self.subject = nil;
	self.descriptionLabel = nil;
	self.description = nil;
	self.categoriesButton = nil;
}

- (void)dealloc
{
	[self viewDidUnload];

	[task release];
	[super dealloc];
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)toInterfaceOrientation
{
	return YES;
}

- (UINavigationItem *)navigationItem
{
	return parentCtrl.navigationItem;
}

- (IBAction)onCategoriesClick:(UIButton *)btn
{
	TaskCategoryPickerController *categoryPicker = [[TaskCategoryPickerController alloc] initWithTask:task];
	[parentCtrl.navigationController pushViewController:categoryPicker animated:YES];
	[categoryPicker release];
}

#pragma mark UITextFieldDelegate protocol

- (BOOL)textFieldShouldReturn:(UITextField *)textField
{
	[textField resignFirstResponder];
	return NO;
}

- (void)textFieldDidEndEditing:(UITextField *)textField
{
	if ([textField.text length])
	{
		task.name = textField.text;
	}
	else
	{
		task.name = _("New task");
		textField.text = task.name;
	}

	[task markDirty];
	NSError *error;
	if (![getManagedObjectContext() save:&error])
	{
		UIAlertView *alert = [[UIAlertView alloc] initWithTitle:_("Error") message:_("Could not save task.") delegate:self cancelButtonTitle:_("OK") otherButtonTitles:nil];
		[alert show];
		[alert release];
	}

	self.navigationItem.title = task.name;
}

#pragma mark UITextViewDelegate protocol

- (BOOL)textViewShouldBeginEditing:(UITextView *)textView
{
	UIBarButtonItem *button = [[UIBarButtonItem alloc] initWithBarButtonSystemItem:UIBarButtonSystemItemSave target:self action:@selector(onSaveDescription:)];
	self.navigationItem.rightBarButtonItem = button;
	[button release];
	
	return YES;
}

- (void)textViewDidEndEditing:(UITextView *)textView
{
	self.navigationItem.rightBarButtonItem = nil;
	[self onSaveDescription:nil];
}

- (void)onSaveDescription:(UIBarButtonItem *)button
{
	[description resignFirstResponder];

	task.longDescription = description.text;
	[task markDirty];
	NSError *error;
	if (![getManagedObjectContext() save:&error])
	{
		UIAlertView *alert = [[UIAlertView alloc] initWithTitle:_("Error") message:_("Could not save task.") delegate:self cancelButtonTitle:_("OK") otherButtonTitles:nil];
		[alert show];
		[alert release];
	}
}

@end
