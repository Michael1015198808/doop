// Generated from org/clyze/doop/jimple/Jimple.g4 by ANTLR 4.9.1

package org.clyze.doop.jimple;

import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link JimpleParser}.
 */
public interface JimpleListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link JimpleParser#program}.
	 * @param ctx the parse tree
	 */
	void enterProgram(JimpleParser.ProgramContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#program}.
	 * @param ctx the parse tree
	 */
	void exitProgram(JimpleParser.ProgramContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#klass}.
	 * @param ctx the parse tree
	 */
	void enterKlass(JimpleParser.KlassContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#klass}.
	 * @param ctx the parse tree
	 */
	void exitKlass(JimpleParser.KlassContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#modifier}.
	 * @param ctx the parse tree
	 */
	void enterModifier(JimpleParser.ModifierContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#modifier}.
	 * @param ctx the parse tree
	 */
	void exitModifier(JimpleParser.ModifierContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#field}.
	 * @param ctx the parse tree
	 */
	void enterField(JimpleParser.FieldContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#field}.
	 * @param ctx the parse tree
	 */
	void exitField(JimpleParser.FieldContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#method}.
	 * @param ctx the parse tree
	 */
	void enterMethod(JimpleParser.MethodContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#method}.
	 * @param ctx the parse tree
	 */
	void exitMethod(JimpleParser.MethodContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#throwsExceptions}.
	 * @param ctx the parse tree
	 */
	void enterThrowsExceptions(JimpleParser.ThrowsExceptionsContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#throwsExceptions}.
	 * @param ctx the parse tree
	 */
	void exitThrowsExceptions(JimpleParser.ThrowsExceptionsContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#identifierList}.
	 * @param ctx the parse tree
	 */
	void enterIdentifierList(JimpleParser.IdentifierListContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#identifierList}.
	 * @param ctx the parse tree
	 */
	void exitIdentifierList(JimpleParser.IdentifierListContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#methodBody}.
	 * @param ctx the parse tree
	 */
	void enterMethodBody(JimpleParser.MethodBodyContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#methodBody}.
	 * @param ctx the parse tree
	 */
	void exitMethodBody(JimpleParser.MethodBodyContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterStatement(JimpleParser.StatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitStatement(JimpleParser.StatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#declarationStmt}.
	 * @param ctx the parse tree
	 */
	void enterDeclarationStmt(JimpleParser.DeclarationStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#declarationStmt}.
	 * @param ctx the parse tree
	 */
	void exitDeclarationStmt(JimpleParser.DeclarationStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#complexAssignmentStmt}.
	 * @param ctx the parse tree
	 */
	void enterComplexAssignmentStmt(JimpleParser.ComplexAssignmentStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#complexAssignmentStmt}.
	 * @param ctx the parse tree
	 */
	void exitComplexAssignmentStmt(JimpleParser.ComplexAssignmentStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#assignmentStmt}.
	 * @param ctx the parse tree
	 */
	void enterAssignmentStmt(JimpleParser.AssignmentStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#assignmentStmt}.
	 * @param ctx the parse tree
	 */
	void exitAssignmentStmt(JimpleParser.AssignmentStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#returnStmt}.
	 * @param ctx the parse tree
	 */
	void enterReturnStmt(JimpleParser.ReturnStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#returnStmt}.
	 * @param ctx the parse tree
	 */
	void exitReturnStmt(JimpleParser.ReturnStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#invokeStmt}.
	 * @param ctx the parse tree
	 */
	void enterInvokeStmt(JimpleParser.InvokeStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#invokeStmt}.
	 * @param ctx the parse tree
	 */
	void exitInvokeStmt(JimpleParser.InvokeStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#allocationStmt}.
	 * @param ctx the parse tree
	 */
	void enterAllocationStmt(JimpleParser.AllocationStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#allocationStmt}.
	 * @param ctx the parse tree
	 */
	void exitAllocationStmt(JimpleParser.AllocationStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#methodSig}.
	 * @param ctx the parse tree
	 */
	void enterMethodSig(JimpleParser.MethodSigContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#methodSig}.
	 * @param ctx the parse tree
	 */
	void exitMethodSig(JimpleParser.MethodSigContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#methodHandle}.
	 * @param ctx the parse tree
	 */
	void enterMethodHandle(JimpleParser.MethodHandleContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#methodHandle}.
	 * @param ctx the parse tree
	 */
	void exitMethodHandle(JimpleParser.MethodHandleContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#methodType}.
	 * @param ctx the parse tree
	 */
	void enterMethodType(JimpleParser.MethodTypeContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#methodType}.
	 * @param ctx the parse tree
	 */
	void exitMethodType(JimpleParser.MethodTypeContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#dynamicMethodSig}.
	 * @param ctx the parse tree
	 */
	void enterDynamicMethodSig(JimpleParser.DynamicMethodSigContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#dynamicMethodSig}.
	 * @param ctx the parse tree
	 */
	void exitDynamicMethodSig(JimpleParser.DynamicMethodSigContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#fieldSig}.
	 * @param ctx the parse tree
	 */
	void enterFieldSig(JimpleParser.FieldSigContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#fieldSig}.
	 * @param ctx the parse tree
	 */
	void exitFieldSig(JimpleParser.FieldSigContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#value}.
	 * @param ctx the parse tree
	 */
	void enterValue(JimpleParser.ValueContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#value}.
	 * @param ctx the parse tree
	 */
	void exitValue(JimpleParser.ValueContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#valueList}.
	 * @param ctx the parse tree
	 */
	void enterValueList(JimpleParser.ValueListContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#valueList}.
	 * @param ctx the parse tree
	 */
	void exitValueList(JimpleParser.ValueListContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#bootValueList}.
	 * @param ctx the parse tree
	 */
	void enterBootValueList(JimpleParser.BootValueListContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#bootValueList}.
	 * @param ctx the parse tree
	 */
	void exitBootValueList(JimpleParser.BootValueListContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#jumpStmt}.
	 * @param ctx the parse tree
	 */
	void enterJumpStmt(JimpleParser.JumpStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#jumpStmt}.
	 * @param ctx the parse tree
	 */
	void exitJumpStmt(JimpleParser.JumpStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#switchStmt}.
	 * @param ctx the parse tree
	 */
	void enterSwitchStmt(JimpleParser.SwitchStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#switchStmt}.
	 * @param ctx the parse tree
	 */
	void exitSwitchStmt(JimpleParser.SwitchStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#caseStmt}.
	 * @param ctx the parse tree
	 */
	void enterCaseStmt(JimpleParser.CaseStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#caseStmt}.
	 * @param ctx the parse tree
	 */
	void exitCaseStmt(JimpleParser.CaseStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#catchStmt}.
	 * @param ctx the parse tree
	 */
	void enterCatchStmt(JimpleParser.CatchStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#catchStmt}.
	 * @param ctx the parse tree
	 */
	void exitCatchStmt(JimpleParser.CatchStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#monitorStmt}.
	 * @param ctx the parse tree
	 */
	void enterMonitorStmt(JimpleParser.MonitorStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#monitorStmt}.
	 * @param ctx the parse tree
	 */
	void exitMonitorStmt(JimpleParser.MonitorStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link JimpleParser#nopStmt}.
	 * @param ctx the parse tree
	 */
	void enterNopStmt(JimpleParser.NopStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link JimpleParser#nopStmt}.
	 * @param ctx the parse tree
	 */
	void exitNopStmt(JimpleParser.NopStmtContext ctx);
}