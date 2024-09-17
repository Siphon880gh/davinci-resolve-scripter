{
	Tools = ordered() {
		Group1 = GroupOperator {
			CtrlWZoom = false,
			Inputs = ordered() {
				Comments = Input { Value = "Before pasting into Fusion:\n- Adjust frame points with fps x clip duration. \nCurrently set to 115 (5 seconds).\n\nAfter pasting into Fusion:\n- Connect MediaIn to INPUT_MED_IN\n- Connect OUTPUT_MED_OUT to MediaOut", },
				Input1 = InstanceInput {
					SourceOp = "INPUT_MED_IN",
					Source = "Background",
				}
			},
			Outputs = {
				Output1 = InstanceOutput {
					SourceOp = "OUTPUT_MED_OUT",
					Source = "Output",
				}
			},
			ViewInfo = GroupInfo {
				Pos = { 302.5, 106.864 },
				Flags = {
					Expanded = true,
					AllowPan = false,
					GridSnap = true,
					AutoSnap = true,
					RemoveRouters = true
				},
				Size = { 621, 198.364, 310.5, 24.2424 },
				Direction = "Horizontal",
				PipeStyle = "Direct",
				Scale = 1,
				Offset = { -302.5, -106.864 }
			},
			Tools = ordered() {
				OUTPUT_MED_OUT = Merge {
					NameSet = true,
					Inputs = {
						Background = Input {
							SourceOp = "Merge1",
							Source = "Output",
						},
						PerformDepthMerge = Input { Value = 0, }
					},
					ViewInfo = OperatorInfo { Pos = { 550, 181.5 } },
				},
				Merge1 = Merge {
					Inputs = {
						Background = Input {
							SourceOp = "GaussianBlur1",
							Source = "Output",
						},
						Foreground = Input {
							SourceOp = "TransformZoomIn",
							Source = "Output",
						},
						PerformDepthMerge = Input { Value = 0, }
					},
					ViewInfo = OperatorInfo { Pos = { 385, 247.5 } },
				},
				GaussianBlur1 = ofx.com.blackmagicdesign.resolvefx.GaussianBlur {
					Inputs = {
						Source = Input {
							SourceOp = "INPUT_MED_IN",
							Source = "Output",
						},
						HStrength = Input { Value = 1, },
						VStrength = Input { Value = 0.400000005960464, },
						Gang = Input { Value = 1, },
						advancedControlsGroup = Input { Value = 1, },
						BorderType = Input { Value = FuID { "BORDER_TYPE_REPLICATE" }, },
						isBlurAlpha = Input { Value = 1, },
						BlendAmount = Input { Value = 0, },
						blendGroup = Input { Value = 0, },
						blendIn = Input { Value = 1, },
						blend = Input { Value = 0, },
						ignoreContentShape = Input { Value = 0, },
						legacyIsProcessRGBOnly = Input { Value = 0, },
						IsNoTemporalFramesReqd = Input { Value = 0, },
						refreshTrigger = Input { Value = 1, },
						srcProcessingAlphaMode = Input { Value = 1, },
						dstProcessingAlphaMode = Input { Value = 1, },
						resolvefxVersion = Input { Value = "3.0", }
					},
					ViewInfo = OperatorInfo { Pos = { 220, 247.5 } },
				},
				TransformTranslate = Transform {
					NameSet = true,
					Inputs = {
						Center = Input {
							SourceOp = "Path1",
							Source = "Position",
						},
						Input = Input {
							SourceOp = "INPUT_MED_IN",
							Source = "Output",
						}
					},
					ViewInfo = OperatorInfo { Pos = { 385, 115.5 } },
				},
				TransformZoomIn = ofx.com.blackmagicdesign.resolvefx.Transform {
					NameSet = true,
					Inputs = {
						Source = Input {
							SourceOp = "TransformTranslate",
							Source = "Output",
						},
						controlMode = Input { Value = FuID { "TransformControlsSliders" }, },
						controlReset = Input { Value = 0, },
						controlGroup = Input { Value = 1, },
						controlVisibility = Input { Value = FuID { "Show" }, },
						posX = Input {
							SourceOp = "TransformZoomInPositionX",
							Source = "Value",
						},
						posY = Input {
							SourceOp = "TransformZoomInPositionY",
							Source = "Value",
						},
						zoom = Input {
							SourceOp = "TransformZoomInZoom",
							Source = "Value",
						},
						rotate = Input { Value = 0, },
						scaleX = Input { Value = 1, },
						scaleY = Input { Value = 1, },
						pitch = Input { Value = 0, },
						yaw = Input { Value = 0, },
						flipH = Input { Value = 0, },
						flipV = Input { Value = 0, },
						adjustGroup = Input { Value = 0, },
						isCrop = Input { Value = 0, },
						cropL = Input { Value = 0, },
						cropR = Input { Value = 0, },
						cropT = Input { Value = 0, },
						cropB = Input { Value = 0, },
						edgeSoftness = Input { Value = 0, },
						edgeRounding = Input { Value = 0, },
						animationGroup = Input { Value = 0, },
						serializedWarpable = Input {
							Value = Text {
							},
						},
						serializedPinnable = Input {
							Value = Text {
							},
						},
						motionBlur = Input { Value = 0, },
						advancedGroup = Input { Value = 0, },
						edgeBehaviour = Input { Value = FuID { "Constant" }, },
						CompositeType = Input { Value = FuID { "COMPOSITE_NORMAL" }, },
						olayAntiAlias = Input { Value = 1, },
						previewAlpha = Input { Value = 0, },
						isLegacyCrop = Input { Value = 0, },
						isLegacyAlphaHandling = Input { Value = 0, },
						isEnforceBlanking = Input { Value = 0, },
						blendGroup = Input { Value = 0, },
						blendIn = Input { Value = 1, },
						blend = Input { Value = 0, },
						ignoreContentShape = Input { Value = 0, },
						legacyIsProcessRGBOnly = Input { Value = 0, },
						IsNoTemporalFramesReqd = Input { Value = 0, },
						refreshTrigger = Input { Value = 1, },
						srcProcessingAlphaMode = Input { Value = -1, },
						dstProcessingAlphaMode = Input { Value = -1, },
						resolvefxVersion = Input { Value = "1.4", }
					},
					ViewInfo = OperatorInfo { Pos = { 385, 181.5 } },
				},
				INPUT_MED_IN = Merge {
					NameSet = true,
					Inputs = {
						PerformDepthMerge = Input { Value = 0, }
					},
					ViewInfo = OperatorInfo { Pos = { 55, 181.5 } },
				}
			},
		},
		Path1 = PolyPath {
			DrawMode = "InsertAndModify",
			CtrlWZoom = false,
			Inputs = {
				Displacement = Input {
					SourceOp = "Path1Displacement",
					Source = "Value",
				},
				PolyLine = Input {
					Value = Polyline {
						Points = {
							{ Linear = true, LockY = true, X = 0, Y = 0, RX = 0.0666666666666667, RY = 0.0666666666666667 },
							{ Linear = true, LockY = true, X = 0.2, Y = 0.2, LX = -0.0666666666666667, LY = -0.0666666666666667, RX = 0, RY = 0 },
							{ Linear = true, LockY = true, X = 0.2, Y = 0.2, LX = 0, LY = 0 }
						}
					},
				}
			},
		},
		Path1Displacement = BezierSpline {
			SplineColor = { Red = 255, Green = 0, Blue = 255 },
			NameSet = true,
			KeyFrames = {
				[0] = { 0, RH = { 38.3333333333333, 0.333333333333333 }, Flags = { LockedY = true } },
				[115] = { 1, LH = { 117.666666666667, 1 }, Flags = { Linear = true, LockedY = true } }
			}
		},
		TransformZoomInPositionX = BezierSpline {
			SplineColor = { Red = 237, Green = 132, Blue = 222 },
			NameSet = true,
			KeyFrames = {
				[0] = { 0, RH = { 38.3333333333333, -0.0666666666666667 }, Flags = { Linear = true } },
				[115] = { -0.2, LH = { 76.6666666666667, -0.133333333333333 }, Flags = { Linear = true } }
			}
		},
		TransformZoomInPositionY = BezierSpline {
			SplineColor = { Red = 237, Green = 132, Blue = 54 },
			NameSet = true,
			KeyFrames = {
				[0] = { 0, RH = { 38.3333333333333, -0.0666666666666667 }, Flags = { Linear = true } },
				[115] = { -0.2, LH = { 76.6666666666667, -0.133333333333333 }, Flags = { Linear = true } }
			}
		},
		TransformZoomInZoom = BezierSpline {
			SplineColor = { Red = 254, Green = 144, Blue = 123 },
			CtrlWZoom = false,
			NameSet = true,
			KeyFrames = {
				[0] = { 1, RH = { 38.3333333333333, 1.13333333333333 }, Flags = { Linear = true } },
				[115] = { 1.4, LH = { 76.6666666666667, 1.26666666666667 }, Flags = { Linear = true } }
			}
		}
	},
	ActiveTool = "Group1"
}
