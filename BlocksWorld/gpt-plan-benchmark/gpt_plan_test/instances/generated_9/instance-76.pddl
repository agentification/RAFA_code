

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a e)
(on b f)
(ontable c)
(on d a)
(on e g)
(on f h)
(on g i)
(ontable h)
(ontable i)
(clear b)
(clear c)
(clear d)
)
(:goal
(and
(on a d)
(on b i)
(on c g)
(on e c)
(on h f)
(on i a))
)
)


