# Swin-S
# model settings
base = 'https://github.com/SwinTransformer/storage/releases/download/v1.0.0'
ckpt = '{}/swin_small_patch4_window7_224.pth'.format(base)
model = dict(type='CascadeRCNN',
             backbone=dict(type='SwinTransformer',
                           embed_dims=96,
                           depths=[2, 2, 18, 2],
                           num_heads=[4, 8, 16, 32],
                           drop_path_rate=0.2,
                           convert_weights=True,
                           init_cfg=dict(type='Pretrained', checkpoint=ckpt)),
             neck=dict(type='FPN',
                       in_channels=[96, 192, 384, 768],
                       out_channels=256, num_outs=5),
             rpn_head=dict(type='RPNHead',
                           in_channels=256,
                           anchor_generator=dict(type='AnchorGenerator',
                                                 scales=[8],
                                                 ratios=[0.5, 1.0, 2.0],
                                                 strides=[4, 8, 16, 32, 64]),
                           bbox_coder=dict(type='DeltaXYWHBBoxCoder',
                                           target_means=[.0, .0, .0, .0],
                                           target_stds=[1.0, 1.0, 1.0, 1.0]),
                           loss_cls=dict(type='CrossEntropyLoss',
                                         use_sigmoid=True, loss_weight=1.0),
                           loss_bbox=dict(type='SmoothL1Loss',
                                          beta=1.0 / 9.0, loss_weight=1.0)),
             roi_head=dict(type='CascadeRoIHead',
                           num_stages=3,
                           stage_loss_weights=[1, 0.5, 0.25],
                           bbox_roi_extractor=dict(type='SingleRoIExtractor',
                                                   roi_layer=dict(type='RoIAlign',
                                                                  output_size=7,
                                                                  sampling_ratio=0),
                                                   out_channels=256,
                                                   featmap_strides=[4, 8, 16, 32]),
                           bbox_head=[dict(type='Shared2FCBBoxHead',
                                           num_classes=10,
                                           reg_class_agnostic=True,
                                           bbox_coder=dict(type='DeltaXYWHBBoxCoder',
                                                           target_means=[0., 0., 0., 0.],
                                                           target_stds=[0.1, 0.1, 0.2, 0.2]),
                                           loss_bbox=dict(type='SmoothL1Loss', beta=1.0, loss_weight=1.0)),
                                      dict(type='Shared2FCBBoxHead',
                                           num_classes=10,
                                           reg_class_agnostic=True,
                                           bbox_coder=dict(type='DeltaXYWHBBoxCoder',
                                                           target_means=[0., 0., 0., 0.],
                                                           target_stds=[0.05, 0.05, 0.1, 0.1]),
                                           loss_bbox=dict(type='SmoothL1Loss', beta=1.0, loss_weight=1.0)),
                                      dict(type='Shared2FCBBoxHead',
                                           num_classes=10,
                                           reg_class_agnostic=True,
                                           bbox_coder=dict(type='DeltaXYWHBBoxCoder',
                                                           target_means=[0., 0., 0., 0.],
                                                           target_stds=[0.033, 0.033, 0.067, 0.067]),
                                           loss_bbox=dict(type='SmoothL1Loss', beta=1.0, loss_weight=1.0))]),
             # model training and testing settings
             train_cfg=dict(rpn=dict(assigner=dict(type='MaxIoUAssigner',
                                                   pos_iou_thr=0.7,
                                                   neg_iou_thr=0.3,
                                                   min_pos_iou=0.3,
                                                   ignore_iof_thr=-1,
                                                   match_low_quality=True),
                                     sampler=dict(type='RandomSampler',
                                                  num=256,
                                                  neg_pos_ub=-1,
                                                  pos_fraction=0.5,
                                                  add_gt_as_proposals=False),
                                     debug=False,
                                     pos_weight=-1,
                                     allowed_border=-1),
                            rpn_proposal=dict(nms=dict(type='nms', iou_threshold=0.7),
                                              nms_pre=2000,
                                              min_bbox_size=0,
                                              max_per_img=1000),
                            rcnn=[dict(assigner=dict(type='MaxIoUAssigner',
                                                     pos_iou_thr=0.5,
                                                     neg_iou_thr=0.5,
                                                     min_pos_iou=0.5,
                                                     ignore_iof_thr=-1,
                                                     match_low_quality=True),
                                       sampler=dict(type='RandomSampler',
                                                    num=512,
                                                    neg_pos_ub=-1,
                                                    pos_fraction=0.25,
                                                    add_gt_as_proposals=True),
                                       debug=False,
                                       mask_size=28,
                                       pos_weight=-1),
                                  dict(assigner=dict(type='MaxIoUAssigner',
                                                     pos_iou_thr=0.6,
                                                     neg_iou_thr=0.6,
                                                     min_pos_iou=0.6,
                                                     ignore_iof_thr=-1,
                                                     match_low_quality=True),
                                       sampler=dict(type='RandomSampler',
                                                    num=512,
                                                    neg_pos_ub=-1,
                                                    pos_fraction=0.25,
                                                    add_gt_as_proposals=True),
                                       debug=False,
                                       mask_size=28,
                                       pos_weight=-1),
                                  dict(assigner=dict(type='MaxIoUAssigner',
                                                     pos_iou_thr=0.7,
                                                     neg_iou_thr=0.7,
                                                     min_pos_iou=0.7,
                                                     ignore_iof_thr=-1,
                                                     match_low_quality=True),
                                       sampler=dict(type='RandomSampler',
                                                    num=512,
                                                    neg_pos_ub=-1,
                                                    pos_fraction=0.25,
                                                    add_gt_as_proposals=True),
                                       debug=False,
                                       mask_size=28,
                                       pos_weight=-1)]),
             test_cfg=dict(rpn=dict(nms=dict(type='nms', iou_threshold=0.7),
                                    nms_pre=1000,
                                    min_bbox_size=0,
                                    max_per_img=1000),
                           rcnn=dict(nms=dict(type='nms', iou_threshold=0.5),
                                     score_thr=0.05,
                                     max_per_img=100)))
# dataset settings
dataset_type = 'ROBINDataset'
data_root = '../Dataset/ROBINv1.1/'
samples_per_gpu = 1
workers_per_gpu = 4
image_norm = dict(mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
train_pipeline = [dict(type='LoadImageFromFile', to_float32=False, color_type='color'),
                  dict(type='LoadAnnotations', with_bbox=True, with_mask=False),
                  dict(type='Resize',
                       img_scale=[(1333, 640), (1333, 800)],
                       multiscale_mode='range', keep_ratio=True),
                  dict(type='RandomFlip', flip_ratio=0.5),
                  dict(type='MixAugment'),
                  dict(type='GridMask'),
                  dict(type='Weather'),
                  dict(type='Normalize', **image_norm),
                  dict(type='Pad', size_divisor=32),
                  dict(type='DefaultFormatBundle'),
                  dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels'])]
test_pipeline = [dict(type='LoadImageFromFile'),
                 dict(type='MultiScaleFlipAug',
                      img_scale=(1333, 800),
                      flip=False,
                      transforms=[dict(type='Resize', keep_ratio=True),
                                  dict(type='RandomFlip'),
                                  dict(type='Normalize', **image_norm),
                                  dict(type='Pad', size_divisor=32),
                                  dict(type='ImageToTensor', keys=['img']),
                                  dict(type='Collect', keys=['img'])])]
data = dict(samples_per_gpu=samples_per_gpu,
            workers_per_gpu=workers_per_gpu,
            train=dict(type=dataset_type,
                       ann_file=data_root + 'train/train.json',
                       pipeline=train_pipeline),
            val=dict(type=dataset_type,
                     ann_file=data_root + 'iid_test/iid.json',
                     pipeline=test_pipeline),
            test=dict(type=dataset_type,
                      ann_file=data_root + 'iid_test/iid.json',
                      pipeline=test_pipeline))
optimizer = dict(type='AdamW', lr=0.0001,
                 betas=(0.9, 0.999), weight_decay=0.05,
                 paramwise_cfg=dict(custom_keys={'norm': dict(decay_mult=0.),
                                                 'absolute_pos_embed': dict(decay_mult=0.),
                                                 'relative_position_bias_table': dict(decay_mult=0.)}))
optimizer_config = dict(grad_clip=None)
fp16 = dict(loss_scale='dynamic')
lr_config = dict(step=[8, 11],
                 policy='step',
                 warmup='linear',
                 warmup_iters=1000,
                 warmup_ratio=0.001)
runner = dict(type='EpochBasedRunner', max_epochs=12)
checkpoint_config = dict(interval=12)
evaluation = dict(interval=12, metric='bbox')
log_config = dict(interval=50, hooks=[dict(type='TextLoggerHook')])
custom_hooks = [dict(type='NumClassCheckHook')]
dist_params = dict(backend='nccl')
log_level = 'INFO'
load_from = None
resume_from = None
workflow = [('train', 1)]
opencv_num_threads = 0
mp_start_method = 'fork'
auto_scale_lr = dict(enable=True, base_batch_size=16)
