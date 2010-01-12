#!/usr/bin/env python

"""Mel support for codeintel.

This file will be imported by the codeintel system on startup and the
register() function called to register this language with the system. All
Code Intelligence for this language is controlled through this module.
"""

import os
import sys
import logging
import operator

from codeintel2.common import *
from codeintel2.citadel import CitadelLangIntel
from codeintel2.langintel import LangIntel
from codeintel2.langintel import (ParenStyleCalltipIntelMixin,
                                  ProgLangTriggerIntelMixin)
from codeintel2.udl import UDLLexer, UDLBuffer, UDLCILEDriver
from codeintel2.util import CompareNPunctLast

from SilverCity.ScintillaConstants import (
    SCE_UDL_SSL_DEFAULT, SCE_UDL_SSL_IDENTIFIER,
    SCE_UDL_SSL_OPERATOR, SCE_UDL_SSL_VARIABLE, SCE_UDL_SSL_WORD,
)

try:
    from xpcom.server import UnwrapObject
    _xpcom_ = True
except ImportError:
    _xpcom_ = False



#---- globals

lang = "Mel"
log = logging.getLogger("codeintel.mel")
#log.setLevel(logging.DEBUG)


# These keywords and builtin functions are copied from "mel-mainlex.udl".

keywords = [
        "and",
        "array",
        "as",
        "case",
        "catch",
        "continue",
        "do",
        "else",
        "exit",
        "float",
        "for",
        "from",
        "global",
        "if",
        "in",
        "int",
        "local",
        "not",
        "of",
        "off",
        "on",
        "or",
        "proc",
        "random",
        "return",
        "select",
        "string",
        "then",
        "throw",
        "to",
        "try",
        "vector",
        "when",
        "where",
        "while",
        "with",
]

builtins = [
        # Built-in functions.
    "about", "abs", "addAttr", "addAttributeEditorNodeHelp", "addDynamic", "addNewShelfTab", "addPP", "addPrefixToName", "addpanelCategory", "advanceToNextDrivenKey", "affectedNet", "affects", "aimConstraint", "air", "alias", "aliasAttr", "align", "alignCtx", "alignCurve", "alignSurface", "allViewFit", "ambientLight", "angle", "angleBetween", "animCone", "animCurveEditor", "animDisplay", "animView", "annotate", "appendStringArray", "applicationName", "applyAttrPreset", "applyTake", "arcLenDimContext", "arcLengthDimension", "arclen", "arrayMapper", "art3dPaintCtx", "artAttrCtx", "artAttrPaintVertexCtx", "artAttrSkinPaintCtx", "artAttrTool", "artBuildPaintMenu", "artFluidAttrCtx", "artPuttyCtx", "artSelectCtx", "artSetPaintCtx", "artUserPaintCtx", "assignCommand", "assignInputDevice", "assignViewportFactories", "attachCurve", "attachDeviceAttr", "attachSurface", "attrColorSliderGrp", "attrCompatibility", "attrControlGrp", "attrEnumOptionMenu", "attrEnumOptionMenuGrp", "attrFieldGrp", "attrFieldSliderGrp", "attrNavigationControlGrp", "attrPresetEditWin", "attributeExists", "attributeInfo", "attributeMenu", "attributeQuery", "autoKeyframe", "autoPlace",
    "bakeClip", "bakeFluidShading", "bakePartialHistory", "bakeResults", "bakeSimulation", "basename", "basenameEx", "batchRender", "bessel", "bevel", "bevelPlus", "binMembership", "bindPose", "bindSkin", "blend2", "blendShape", "blendShapeEditor", "blendShapePanel", "blendTwoAttr", "blindDataType", "boneLattice", "boundary", "boxDollyCtx", "boxZoomCtx", "bufferCurve", "buildBookmarkMenu", "buildKeyframeMenu", "button", "buttonManip",
    "CBG", "cacheFile", "cacheFileCombine", "cacheFileMerge", "cacheFileTrack", "camera", "cameraView", "canCreateManip", "canvas", "capitalizeString", "catch", "catchQuiet", "ceil", "changeSubdivComponentDisplayLevel", "changeSubdivRegion", "channelBox", "character", "characterMap", "characterOutlineEditor", "characterize", "chdir", "checkBox", "checkBoxGrp", "checkDefaultRenderGlobals", "choice", "circle", "circularFillet", "clamp", "clear", "clearCache", "clip", "clipEditor", "clipEditorCurrentTimeCtx", "clipSchedule", "clipSchedulerOutliner", "clipTrimBefore", "closeCurve", "closeSurface", "cluster", "cmdFileOutput", "cmdScrollFieldExecuter", "cmdScrollFieldReporter", "cmdShell", "coarsenSubdivSelectionList", "collision", "color", "colorAtPoint", "colorEditor", "colorIndex", "colorIndexSliderGrp", "colorSliderButtonGrp", "colorSliderGrp", "columnLayout", "commandEcho", "commandLine", "commandPort", "compactHairSystem", "componentEditor", "compositingInterop", "computePolysetVolume", "condition", "cone", "confirmDialog", "connectAttr", "connectControl", "connectDynamic", "connectJoint", "connectionInfo", "constrain", "constrainValue", "constructionHistory", "containerNodeInfo", "contextInfo", "control", "convertFromOldLayers", "convertIffToPsd", "convertLightmap", "convertSolidTx", "convertTessellation", "convertUnit", "copyArray", "copyFlexor", "copyKey", "copySkinWeights", "cos", "cpButton", "cpCache", "cpClothSet", "cpCollision", "cpConstraint", "cpConvClothToMesh", "cpForces", "cpGetSolverAttr", "cpPanel", "cpProperty", "cpRigidCollisionFilter", "cpSeam", "cpSetEdit", "cpSetSolverAttr", "cpSolver", "cpSolverTypes", "cpTool", "cpUpdateClothUVs", "createDisplayLayer", "createDrawCtx", "createEditor", "createLayeredPsdFile", "createMotionField", "createNewShelf", "createNode", "createRenderLayer", "createSubdivRegion", "cross", "crossProduct", "ctxAbort", "ctxCompletion", "ctxEditMode", "ctxTraverse", "currentCtx", "currentTime", "currentTimeCtx", "currentUnit", "curve", "curveAddPtCtx", "curveCVCtx", "curveEPCtx", "curveEditorCtx", "curveIntersect", "curveMoveEPCtx", "curveOnSurface", "curveSketchCtx", "cutKey", "cycleCheck", "cylinder",
    "date", "dagPose", "defaultLightListCheckBox", "defaultNavigation", "defineDataServer", "defineVirtualDevice", "deformer", "deg_to_rad", "delete", "deleteAttr", "deleteShadingGroupsAndMaterials", "deleteShelfTab", "deleteUI", "deleteUnusedBrushes", "delrandstr", "detachCurve", "detachDeviceAttr", "detachSurface", "deviceEditor", "devicePanel", "dgInfo", "dgdirty", "dgeval", "dgtimer", "dimWhen", "directKeyCtx", "directionalLight", "dirmap", "dirname", "disable", "disconnectAttr", "disconnectJoint", "diskCache", "displacementToPoly", "displayAffected", "displayColor", "displayCull", "displayLevelOfDetail", "displayPref", "displayRGBColor", "displaySmoothness", "displayStats", "displaySurface", "distanceDimContext", "distanceDimension", "doBlur", "docServer", "dolly", "dollyCtx", "dopeSheetEditor", "dot", "dotProduct", "doubleProfileBirailSurface", "drag", "dragAttrContext", "draggerContext", "dropoffLocator", "duplicate", "duplicateCurve", "duplicateSurface", "dynCache", "dynControl", "dynExport", "dynExpression", "dynGlobals", "dynPaintEditor", "dynParticleCtx", "dynPref", "dynRelEdPanel", "dynRelEditor", "dynamicLoad",
    "editAttrLimits", "editDisplayLayerGlobals", "editDisplayLayerMembers", "editRenderLayerAdjustment", "editRenderLayerGlobals", "editRenderLayerMembers", "editor", "editorTemplate", "effector", "emit", "emitter", "enableDevice", "encodeString", "endString", "endsWith", "env", "equivalent", "equivalentTol", "erf", "error", "eval", "evalDeferred", "evalEcho", "event", "exactWorldBoundingBox", "exclusiveLightCheckBox", "exec", "executeForEachObject", "exists", "exp", "exportComposerCurves", "expression", "expressionEditorListen", "extendCurve", "extendSurface", "extrude",
    "fcheck", "fclose", "feof", "fflush", "fgetline", "fgetword", "file", "fileBrowserDialog", "fileDialog", "fileExtension", "fileInfo", "filetest", "filletCurve", "filter", "filterCurve", "filterExpand", "filterStudioImport", "findAllIntersections", "findAnimCurves", "findKeyframe", "findMenuItem", "findRelatedSkinCluster", "finder", "firstParentOf", "fitBspline", "flexor", "floatEq", "floatField", "floatFieldGrp", "floatScrollBar", "floatSlider", "floatSlider2", "floatSliderButtonGrp", "floatSliderGrp", "floor", "flow", "fluidCacheInfo", "fluidEmitter", "fluidVoxelInfo", "flushUndo", "fmod", "fontDialog", "fopen", "formLayout", "format", "fprint", "frameLayout", "fread", "freeFormFillet", "frewind", "fromNativePath", "fwrite",
    "gamma", "gauss", "geometryConstraint", "getApplicationVersionAsFloat", "getAttr", "getClassification", "getDefaultBrush", "getFileList", "getFluidAttr", "getInputDeviceRange", "getMayaPanelTypes", "getModifiers", "getPanel", "getParticleAttr", "getenv", "getpid", "glRender", "glRenderEditor", "globalStitch", "gmatch", "goal", "gotoBindPose", "grabColor", "gradientControl", "gradientControlNoAttr", "graphDollyCtx", "graphSelectContext", "graphTrackCtx", "gravity", "grid", "gridLayout", "group", "groupObjectsByName",
    "HfAddAttractorToAS", "HfAssignAS", "HfBuildEqualMap", "HfBuildFurFiles", "HfBuildFurImages", "HfCancelAFR", "HfConnectASToHF", "HfCreateAttractor", "HfDeleteAS", "HfEditAS", "HfPerformCreateAS", "HfRemoveAttractorFromAS", "HfSelectAttached", "HfSelectAttractors", "HfUnAssignAS", "hardenPointCurve", "hardware", "hardwareRenderPanel", "headsUpDisplay", "headsUpMessage", "help", "helpLine", "hermite", "hide", "hilite", "hitTest", "hotBox", "hotkey", "hotkeyCheck", "hsv_to_rgb", "hudButton", "hudSlider", "hudSliderButton", "hwReflectionMap", "hwRender", "hwRenderLoad", "hyperGraph", "hyperPanel", "hyperShade", "hypot",
    "iconTextButton", "iconTextCheckBox", "iconTextRadioButton", "iconTextRadioCollection", "iconTextScrollList", "iconTextStaticLabel", "ikHandle", "ikHandleCtx", "ikHandleDisplayScale", "ikSolver", "ikSplineHandleCtx", "ikSystem", "ikSystemInfo", "ikfkDisplayMethod", "illustratorCurves", "image", "imfPlugins", "importComposerCurves", "inheritTransform", "insertJoint", "insertJointCtx", "insertKeyCtx", "insertKnotCurve", "insertKnotSurface", "instance", "instanceable", "instancer", "intField", "intFieldGrp", "intScrollBar", "intSlider", "intSliderGrp", "interToUI", "internalVar", "intersect", "iprEngine", "isAnimCurve", "isConnected", "isDirty", "isParentOf", "isSameObject", "isTrue", "isValidObjectName", "isValidString", "isValidUiName", "isolateSelect", "itemFilter", "itemFilterAttr", "itemFilterRender", "itemFilterType",
    "joint", "jointCluster", "jointCtx", "jointDisplayScale", "jointLattice",
    "keyTangent", "keyframe", "keyframeOutliner", "keyframeRegionCurrentTimeCtx", "keyframeRegionDirectKeyCtx", "keyframeRegionDollyCtx", "keyframeRegionInsertKeyCtx", "keyframeRegionMoveKeyCtx", "keyframeRegionScaleKeyCtx", "keyframeRegionSelectKeyCtx", "keyframeRegionSetKeyCtx", "keyframeRegionTrackCtx", "keyframeStats",
    "lassoContext", "lattice", "latticeDeformKeyCtx", "launch", "launchImageEditor", "layerButton", "layeredShaderPort", "layeredTexturePort", "layout", "layoutDialog", "lightList", "lightListEditor", "lightListPanel", "lightlink", "lineIntersection", "linearPrecision", "linstep", "listAnimatable", "listAttr", "listCameras", "listConnections", "listDeviceAttachments", "listHistory", "listInputDeviceAxes", "listInputDeviceButtons", "listInputDevices", "listMenuAnnotation", "listNodeTypes", "listRelatives", "listSets", "listTransforms", "listUnselected", "listerEditor", "listpanelCategories", "loadFluid", "loadNewShelf", "loadPlugin", "loadPrefObjects", "lockNode", "loft", "log", "longNameOf", "lookThru", "ls", "lsThroughFilter", "lsType", "lsUI",
    "Mayatomr", "mag", "makeIdentity", "makeLive", "makePaintable", "makeRoll", "makeSingleSurface", "makeTubeOn", "makebot", "manipMoveContext", "manipMoveLimitsCtx", "manipOptions", "manipRotateContext", "manipRotateLimitsCtx", "manipScaleContext", "manipScaleLimitsCtx", "marker", "match", "max", "memory", "menu", "menuBarLayout", "menuEditor", "menuItem", "menuItemToShelf", "menuSet", "menuSetPref", "messageLine", "min", "minimizeApp", "mirrorJoint", "modelCurrentTimeCtx", "modelEditor", "modelPanel", "mouse", "movIn", "movOut", "move", "moveIKtoFK", "moveKeyCtx", "moveVertexAlongDirection", "multiProfileBirailSurface", "mute",
    "nParticle", "nameCommand", "nameField", "namespace", "namespaceInfo", "newPanelItems", "newton", "nodeCast", "nodeIconButton", "nodeOutliner", "nodePreset", "nodeType", "noise", "nonLinear", "normalConstraint", "normalize", "nurbsBoolean", "nurbsCopyUVSet", "nurbsCube", "nurbsEditUV", "nurbsPlane", "nurbsSelect", "nurbsSquare", "nurbsToPoly", "nurbsToPolygonsPref", "nurbsToSubdiv", "nurbsUVSet", "nurbsViewDirectionVector",
    "objExists", "objectCenter", "objectLayer", "objectType", "objectTypeUI", "obsoleteProc", "oceanNurbsPreviewPlane", "offsetCurve", "offsetCurveOnSurface", "offsetSurface", "openGLExtension", "openMayaPref", "optionMenu", "optionMenuGrp", "optionVar", "orbit", "orbitCtx", "orientConstraint", "outlinerEditor", "outlinerPanel", "overrideModifier",
    "paintEffectsDisplay", "pairBlend", "palettePort", "paneLayout", "panel", "panelConfiguration", "panelHistory", "paramDimContext", "paramDimension", "paramLocator", "parent", "parentConstraint", "particle", "particleExists", "particleInstancer", "particleRenderInfo", "partition", "pasteKey", "pathAnimation", "pause", "pclose", "percent", "performanceOptions", "pfxstrokes", "pickWalk", "picture", "pixelMove", "planarSrf", "plane", "play", "playbackOptions", "playblast", "plugAttr", "plugNode", "pluginInfo", "pointConstraint", "pointCurveConstraint", "pointLight", "pointMatrixMult", "pointOnCurve", "pointOnSurface", "pointPosition", "poleVectorConstraint", "polyAppend", "polyAppendFacetCtx", "polyAppendVertex", "polyAutoProjection", "polyAverageNormal", "polyAverageVertex", "polyBevel", "polyBlendColor", "polyBlindData", "polyBoolOp", "polyBridgeEdge", "polyCacheMonitor", "polyCheck", "polyChipOff", "polyClipboard", "polyCloseBorder", "polyCollapseEdge", "polyCollapseFacet", "polyColorBlindData", "polyColorPerVertex", "polyColorSet", "polyCompare", "polyCone", "polyCopyUV", "polyCrease", "polyCreaseCtx", "polyCreateFacet", "polyCreateFacetCtx", "polyCube", "polyCut", "polyCutCtx", "polyCylinder", "polyCylindricalProjection", "polyDelEdge", "polyDelFacet", "polyDelVertex", "polyDuplicateAndConnect", "polyDuplicateEdge", "polyEditUV", "polyEditUVShell", "polyEvaluate", "polyExtrudeEdge", "polyExtrudeFacet", "polyFlipEdge", "polyFlipUV", "polyForceUV", "polyGeoSampler", "polyHelix", "polyInfo", "polyInstallAction", "polyLayoutUV", "polyListComponentConversion", "polyMapCut", "polyMapDel", "polyMapSew", "polyMapSewMove", "polyMergeEdge", "polyMergeEdgeCtx", "polyMergeFacet", "polyMergeFacetCtx", "polyMergeUV", "polyMergeVertex", "polyMirrorFace", "polyMoveEdge", "polyMoveFacet", "polyMoveFacetUV", "polyMoveUV", "polyMoveVertex", "polyNormal", "polyNormalPerVertex", "polyNormalizeUV", "polyOptions", "polyOutput", "polyPipe", "polyPlanarProjection", "polyPlane", "polyPlatonicSolid", "polyPoke", "polyPrism", "polyProjection", "polyPyramid", "polyQuad", "polyQueryBlindData", "polyReduce", "polySelect", "polySelectConstraint", "polySelectConstraintMonitor", "polySelectCtx", "polySelectEditCtx", "polySeparate", "polySetToFaceNormal", "polySewEdge", "polyShortestPathCtx", "polySmooth", "polySoftEdge", "polySphere", "polySphericalProjection", "polySplit", "polySplitCtx", "polySplitEdge", "polySplitRing", "polySplitVertex", "polyStraightenUVBorder", "polySubdivideEdge", "polySubdivideFacet", "polySuperCtx", "polyToSubdiv", "polyTorus", "polyTransfer", "polyTriangulate", "polyUVSet", "polyUnite", "polyWedgeFace", "popen", "popupMenu", "pose", "pow", "preloadRefEd", "print", "progressBar", "progressWindow", "projFileViewer", "projectCurve", "projectTangent", "projectionContext", "projectionManip", "promptDialog", "propModCtx", "propMove", "psdChannelOutliner", "psdEditTextureFile", "psdExport", "psdTextureFile", "putenv", "pwd", "python",
    "querySubdiv", "quit",
    "rad_to_deg", "radial", "radioButton", "radioButtonGrp", "radioCollection", "radioMenuItemCollection", "rampColorPort", "rand", "randomizeFollicles", "randstate", "rangeControl", "readTake", "rebuildCurve", "rebuildSurface", "recordAttr", "recordDevice", "redo", "reference", "referenceEdit", "referenceQuery", "refineSubdivSelectionList", "refresh", "refreshAE", "rehash", "reloadImage", "removeJoint", "removeMultiInstance", "removepanelCategory", "rename", "renameAttr", "renameSelectionList", "renameUI", "render", "renderGlobalsNode", "renderInfo", "renderLayerButton", "renderLayerParent", "renderLayerPostProcess", "renderLayerUnparent", "renderManip", "renderPartition", "renderQualityNode", "renderSettings", "renderThumbnailUpdate", "renderWindowEditor", "renderWindowSelectContext", "renderer", "reorder", "reorderDeformers", "requires", "reroot", "resampleFluid", "resetAE", "resetPfxToPolyCamera", "resetTool", "resolutionNode", "retarget", "reverseCurve", "reverseSurface", "revolve", "rgb_to_hsv", "rigidBody", "rigidSolver", "roll", "rollCtx", "rootOf", "rot", "rotate", "rotationInterpolation", "roundConstantRadius", "rowColumnLayout", "rowLayout", "runTimeCommand", "runup",
    "sampleImage", "saveAllShelves", "saveAttrPreset", "saveFluid", "saveImage", "saveInitialState", "saveMenu", "savePrefObjects", "savePrefs", "saveShelf", "saveToolSettings", "scale", "scaleBrushBrightness", "scaleComponents", "scaleConstraint", "scaleKey", "scaleKeyCtx", "sceneEditor", "sceneUIReplacement", "scmh", "scriptCtx", "scriptEditorInfo", "scriptJob", "scriptNode", "scriptTable", "scriptToShelf", "scriptedPanel", "scriptedPanelType", "scrollField", "scrollLayout", "sculpt", "searchPathArray", "seed", "selLoadSettings", "select", "selectContext", "selectKey", "selectKeyCtx", "selectKeyframeRegionCtx", "selectMode", "selectPref", "selectPriority", "selectType", "selectedNodes", "selectionConnection", "separator", "setAttr", "setAttrMapping", "setConstraintRestPosition", "setDefaultShadingGroup", "setDrivenKeyframe", "setDynamic", "setEditCtx", "setEditor", "setEscapeCtx", "setFluidAttr", "setFocus", "setInfinity", "setInputDeviceMapping", "setKeyCtx", "setKeyPath", "setKeyframe", "setKeyframeBlendshapeTargetWts", "setMenuMode", "setNodeTypeFlag", "setParent", "setParticleAttr", "setPfxToPolyCamera", "setProject", "setStampDensity", "setStartupMessage", "setState", "setToolTo", "setUITemplate", "setXformManip", "sets", "shadingConnection", "shadingGeometryRelCtx", "shadingLightRelCtx", "shadingNetworkCompare", "shadingNode", "shapeCompare", "shelfButton", "shelfLayout", "shelfTabLayout", "shellField", "shortNameOf", "showHelp", "showHidden", "showManipCtx", "showSelectionInTitle", "showShadingGroupAttrEditor", "showWindow", "sign", "simplify", "sin", "singleProfileBirailSurface", "size", "skinCluster", "skinPercent", "smoothCurve", "smoothTangentSurface", "smoothstep", "snap2to2", "snapKey", "snapMode", "snapTogetherCtx", "snapshot", "soft", "softMod", "softModCtx", "sort", "sound", "soundControl", "source", "spaceLocator", "sphere", "sphrand", "spotLight", "spotLightPreviewPort", "spreadSheetEditor", "spring", "sqrt", "squareSurface", "srtContext", "stackTrace", "startString", "startsWith", "stitchAndExplodeShell", "stitchSurface", "stitchSurfacePoints", "strcmp", "stringArrayCatenate", "stringArrayContains", "stringArrayCount", "stringArrayInsertAtIndex", "stringArrayIntersector", "stringArrayRemove", "stringArrayRemoveAtIndex", "stringArrayRemoveExact", "stringArrayRemoveDuplicates", "stringArrayToString", "stringToStringArray", "strip", "stripPrefixFromName", "stroke", "subdAutoProjection", "subdCleanTopology", "subdCollapse", "subdDuplicateAndConnect", "subdEditUV", "subdListComponentConversion", "subdMapCut", "subdMapSewMove", "subdMatchTopology", "subdMirror", "subdToBlind", "subdToPoly", "subdTransferUVsToCache", "subdiv", "subdivCrease", "subdivDisplaySmoothness", "substitute", "substituteAllString", "substituteGeometry", "substring", "superCtx", "surface", "surfaceSampler", "surfaceShaderList", "swatchDisplayPort", "switchTable", "symbolButton", "symbolCheckBox", "sysFile", "system",
    "tabLayout", "tan", "tangentConstraint", "texLatticeDeformContext", "texManipContext", "texMoveContext", "texMoveUVShellContext", "texRotateContext", "texScaleContext", "texSelectContext", "texSelectShortestPathCtx", "texSmudgeUVContext", "texWinToolCtx", "text", "textCurves", "textField", "textFieldButtonGrp", "textFieldGrp", "textManip", "textScrollList", "textToShelf", "textureDisplacePlane", "textureHairColor", "texturePlacementContext", "textureWindow", "threadCount", "threePointArcCtx", "timeControl", "timePort", "timerX", "toNativePath", "toggle", "toggleAxis", "toggleWindowVisibility", "tokenize", "tokenizeList", "tolerance", "tolower", "toolButton", "toolCollection", "toolDropped", "toolHasOptions", "toolPropertyWindow", "torus", "toupper", "trace", "track", "trackCtx", "transferAttributes", "transformCompare", "transformLimits", "translator", "trim", "trunc", "truncateFluidCache", "truncateHairCache", "tumble", "tumbleCtx", "turbulence", "twoPointArcCtx",
    "uiRes", "uiTemplate", "unassignInputDevice", "undo", "undoInfo", "ungroup", "uniform", "unit", "unloadPlugin", "untangleUV", "untrim", "upAxis", "updateAE", "userCtx", "uvLink", "uvSnapshot",
    "validateShelfName", "vectorize", "verifyCmd", "view2dToolCtx", "viewCamera", "viewClipPlane", "viewFit", "viewHeadOn", "viewLookAt", "viewPlace", "viewSet", "visor", "volumeAxis", "vortex",
    "waitCursor", "warning", "webBrowser", "webBrowserPrefs", "whatIs", "window", "windowPref", "wire", "wireContext", "workspace", "wrinkle", "wrinkleContext", "writeTake",
    "xbmLangPathList", "xform", "xpmPicker",
]

#---- Lexer class

# Dev Notes:
# Komodo's editing component is based on scintilla (scintilla.org). This
# project provides C++-based lexers for a number of languages -- these
# lexers are used for syntax coloring and folding in Komodo. Komodo also
# has a UDL system for writing UDL-based lexers that is simpler than
# writing C++-based lexers and has support for multi-language files.
#
# The codeintel system has a Lexer class that is a wrapper around these
# lexers. You must define a Lexer class for lang Mel. If Komodo's
# scintilla lexer for Mel is UDL-based, then this is simply:
#
#   from codeintel2.udl import UDLLexer
#   class MelLexer(UDLLexer):
#       lang = lang
#
# Otherwise (the lexer for Mel is one of Komodo's existing C++ lexers
# then this is something like the following. See lang_python.py or
# lang_perl.py in your Komodo installation for an example. "SilverCity"
# is the name of a package that provides Python module APIs for Scintilla
# lexers.
#
#   import SilverCity
#   from SilverCity.Lexer import Lexer
#   from SilverCity import ScintillaConstants
#   class MelLexer(Lexer):
#       lang = lang
#       def __init__(self):
#           self._properties = SilverCity.PropertySet()
#           self._lexer = SilverCity.find_lexer_module_by_id(ScintillaConstants.SCLEX_MEL)
#           self._keyword_lists = [
#               # Dev Notes: What goes here depends on the C++ lexer
#               # implementation.
#           ]

class MelLexer(UDLLexer):
    lang = lang

#---- LangIntel class

# Dev Notes:
# All language should define a LangIntel class. (In some rare cases it
# isn't needed but there is little reason not to have the empty subclass.)
#
# One instance of the LangIntel class will be created for each codeintel
# language. Code browser functionality and some buffer functionality
# often defers to the LangIntel singleton.
#
# This is especially important for multi-lang files. For example, an
# HTML buffer uses the JavaScriptLangIntel and the CSSLangIntel for
# handling codeintel functionality in <script> and <style> tags.
#
# See other lang_*.py files in your Komodo installation for examples of
# usage.

class MelLangIntel(CitadelLangIntel, ParenStyleCalltipIntelMixin,
                   ProgLangTriggerIntelMixin):
    lang = lang

    # Used by ProgLangTriggerIntelMixin.preceding_trg_from_pos()
    trg_chars = tuple('$(')
    calltip_trg_chars = tuple('(')

    ##
    # Implicit triggering event, i.e. when typing in the editor.
    #
    def trg_from_pos(self, buf, pos, implicit=True, DEBUG=False, ac=None):
        #DEBUG = True
        if pos < 1:
            return None

        accessor = buf.accessor
        last_pos = pos-1
        char = accessor.char_at_pos(last_pos)
        style = accessor.style_at_pos(last_pos)
        if DEBUG:
            print "trg_from_pos: char: %r, style: %d" % (char, accessor.style_at_pos(last_pos), )
        if char == '$':
            # Variable completion trigger.
            if DEBUG:
                print "triggered:: complete variables"
            return Trigger(self.lang, TRG_FORM_CPLN, "variables",
                           pos, implicit)
        elif style in (SCE_UDL_SSL_WORD, SCE_UDL_SSL_IDENTIFIER):
            # Functions/builtins completion trigger.
            start, end = accessor.contiguous_style_range_from_pos(last_pos)
            if DEBUG:
                print "identifier style, start: %d, end: %d" % (start, end)
            # Trigger when two characters have been typed.
            if (last_pos - start) == 1:
                if DEBUG:
                    print "triggered:: complete identifiers"
                return Trigger(self.lang, TRG_FORM_CPLN, "identifiers",
                               start, implicit)
        return None

    ##
    # Explicit triggering event, i.e. Ctrl+J.
    #
    def preceding_trg_from_pos(self, buf, pos, curr_pos,
                               preceding_trg_terminators=None, DEBUG=False):
        #DEBUG = True
        if pos < 1:
            return None

        accessor = buf.accessor
        last_pos = pos-1
        char = accessor.char_at_pos(last_pos)
        style = accessor.style_at_pos(last_pos)
        if DEBUG:
            print "pos: %d, curr_pos: %d" % (pos, curr_pos)
            print "char: %r, style: %d" % (char, style)
        if char == '$':
             return Trigger(self.lang, TRG_FORM_CPLN, "variables",
                            pos, implicit=False)
        if style in (SCE_UDL_SSL_VARIABLE, ):
            start, end = accessor.contiguous_style_range_from_pos(last_pos)
            if DEBUG:
                print "triggered:: complete variables"
            return Trigger(self.lang, TRG_FORM_CPLN, "variables",
                           start+1, implicit=False)
        elif style in (SCE_UDL_SSL_WORD, SCE_UDL_SSL_IDENTIFIER):
            # Functions/builtins completion trigger.
            start, end = accessor.contiguous_style_range_from_pos(last_pos)
            if DEBUG:
                print "triggered:: complete identifiers"
            return Trigger(self.lang, TRG_FORM_CPLN, "identifiers",
                           start, implicit=False)
        return None

    ##
    # Provide the list of completions or the calltip string.
    # Completions are a list of tuple (type, name) items.
    #
    # Note: This example is *not* asynchronous.
    def async_eval_at_trg(self, buf, trg, ctlr):
        if _xpcom_:
            trg = UnwrapObject(trg)
            ctlr = UnwrapObject(ctlr)
        pos = trg.pos
        ctlr.start(buf, trg)

        if trg.id == (self.lang, TRG_FORM_CPLN, "variables"):
            # Find all variables in the current file, complete using them.
            ctlr.set_cplns(self._get_all_variables_in_buffer(buf))
            ctlr.done("success")
            return

        if trg.id == (self.lang, TRG_FORM_CPLN, "identifiers"):
            # Return all known keywords and builtins.
            ctlr.set_cplns(self._get_all_known_identifiers(buf))
            ctlr.done("success")
            return

        ctlr.error("Unknown trigger type: %r" % (trg, ))
        ctlr.done("error")

    ##
    # Internal functions
    #

    def _get_all_variables_in_buffer(self, buf):
        all_variables = set()
        for token in buf.accessor.gen_tokens():
            if token.get('style') == SCE_UDL_SSL_VARIABLE:
                all_variables.add(token.get('text')[1:])
        return [("variable", x) for x in sorted(all_variables, cmp=CompareNPunctLast)]

    _identifier_cplns = None
    def _get_all_known_identifiers(self, buf):
        if MelLangIntel._identifier_cplns is None:
            cplns = [("keyword", x) for x in keywords]
            cplns += [("function", x) for x in builtins]
            MelLangIntel._identifier_cplns = sorted(cplns, cmp=CompareNPunctLast, key=operator.itemgetter(1))
        return MelLangIntel._identifier_cplns

#---- Buffer class

# Dev Notes:
# Every language must define a Buffer class. An instance of this class
# is created for every file of this language opened in Komodo. Most of
# that APIs for scanning, looking for autocomplete/calltip trigger points
# and determining the appropriate completions and calltips are called on
# this class.
#
# Currently a full explanation of these API is beyond the scope of this
# stub. Resources for more info are:
# - the base class definitions (Buffer, CitadelBuffer, UDLBuffer) for
#   descriptions of the APIs
# - lang_*.py files in your Komodo installation as examples
# - the upcoming "Anatomy of a Komodo Extension" tutorial
# - the Komodo community forums:
#   http://community.activestate.com/products/Komodo
# - the Komodo discussion lists:
#   http://listserv.activestate.com/mailman/listinfo/komodo-discuss
#   http://listserv.activestate.com/mailman/listinfo/komodo-beta
#
class MelBuffer(UDLBuffer):
    # Dev Note: What to sub-class from?
    # - If this is a UDL-based language: codeintel2.udl.UDLBuffer
    # - Else if this is a programming language (it has functions,
    #   variables, classes, etc.): codeintel2.citadel.CitadelBuffer
    # - Otherwise: codeintel2.buffer.Buffer
    lang = lang

    cb_show_if_empty = True

    #cpln_fillup_chars = " '\";},>"
    cpln_stop_chars = "~`!$@#%^&*()-=+{}[]|\\;:'\",.<>?/ "

    # Dev Note: many details elided.


#---- CILE Driver class

# Dev Notes:
# A CILE (Code Intelligence Language Engine) is the code that scans
# Mel content and returns a description of the code in that file.
# See "cile_mel.py" for more details.
#
# The CILE Driver is a class that calls this CILE. If Mel is
# multi-lang (i.e. can contain sections of different language content,
# e.g. HTML can contain markup, JavaScript and CSS), then you will need
# to also implement "scan_multilang()".
class MelCILEDriver(UDLCILEDriver):
    lang = lang

    def scan_purelang(self, buf):
        import cile_mel
        return cile_mel.scan_buf(buf)

    def scan_multilang(self, buf, csl_cile_driver=None):
        """Scan the given multilang (UDL-based) buffer and return a CIX
        element tree.

            "buf" is the multi-lang Buffer instance (e.g.
                lang_rhtml.RHTMLBuffer for RHTML).
            "csl_cile_driver" (optional) is the CSL (client-side language)
                CILE driver. While scanning, CSL tokens should be gathered and,
                if any, passed to the CSL scanner like this:
                    csl_cile_driver.scan_csl_tokens(
                        file_elem, blob_name, csl_tokens)
                The CSL scanner will append a CIX <scope ilk="blob"> element
                to the <file> element.
        """
        import cile_mel
        return cile_mel.scan_buf(buf)


#---- registration

def register(mgr):
    """Register language support with the Manager."""
    mgr.set_lang_info(
        lang,
        silvercity_lexer=MelLexer(),
        buf_class=MelBuffer,
        langintel_class=MelLangIntel,
        import_handler_class=None,
        cile_driver_class=MelCILEDriver,
        # Dev Note: set to false if this language does not support
        # autocomplete/calltips.
        is_cpln_lang=True)

