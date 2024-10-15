#defined team/2.
#defined pref/3.

%#const students_per_topic = 3.

% Assign at most students_per_topic students to each topic.
{ assign(S, T) : student(S) } students_per_topic :- topic(T).

% Do not assign the same student to two different topics.
:- assign(S, T1), assign(S, T2), T1 != T2.
% Every student must be assigned to a topic.
:- student(S), not assign(S, T) : topic(T).
% Students in a team must be assigned the same topic.
:- team(S1, S2), assign(S1, T1), assign(S2, T2), T1 != T2.


% OPTIMIZATION
% Disallow assignments where swapping topics would be better for both students.
:- assign(S1,T1), assign(S2,T2), not team(S1,_), not team(S2, _), not own(S1,T1), not own(S2,T2), pref(S1,T1,P11), pref(S1,T2,P12), pref(S2,T1,P21), pref(S2,T2,P22), P12 < P11, P21 < P22.
:- assign(S1,T1), assign(S2,T2), not team(S1,_), not team(S2, _), not own(S1,T1), not own(S2,T2), not pref(S1,T1,_), pref(S1,T2,_), pref(S2,T1,_), not pref(S2,T2,_).

error("Inconsistent teams", (S1, S2)) :- team(S1, S2), not team(S2, S1).
error("Multiple teams", S) :- student(S), #count { S1 : team(S, S1) } > students_per_topic.
error("Inconsistent preferences", (S, T, P1, P2)) :- pref(S, T, P1), pref(S, T, P2), P1 != P2.

% Assign students to the topic they proposed.
#maximize { 1@4,S : own(S,T), assign(S, T) }.
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
