#defined team/2.
#defined pref/3.

#const students_per_topic = 2.

% Assign at most students_per_topic students to each topic.
{ assign(S, T) : student(S) } students_per_topic :- topic(T).

% Do not assign the same student to two different topics.
:- assign(S, T1), assign(S, T2), T1 != T2.
% Every student must be assigned to a topic.
:- student(S), not assign(S, T) : topic(T).
% Students in a team must be assigned the same topic.
:- team(S1, S2), assign(S1, T1), assign(S2, T2), T1 != T2.

error("Inconsistent teams", (S1, S2)) :- team(S1, S2), not team(S2, S1).
error("Multiple teams", S) :- team(S, S1), team(S, S2), S1 != S2.
error("Inconsistent preferences", (S, T, P1, P2)) :- pref(S, T, P1), pref(S, T, P2), P1 != P2.

% Maximize the number of students assigned to a topic (up to students_per_topic many).
#maximize { 1@2,S1,T : assign(S,T), assign(S1,T), S < S1 }.
% Minimize the number of assignments of unranked topics
% (i.e., the student did not give any preference for the assigned topic).
#minimize { 1,S,T2 : assign(S,T1), not pref(S,T1,_), pref(S,T2,P) }.
% Minimize the number of sub-optimal assignments
% (i.e., better ranked topics not assigned to a student).
#minimize { 1,S,T2 : assign(S,T1), pref(S,T1,P1), pref(S,T2,P2), P2 < P1 }.

#show assign/2.
#show error/2.
