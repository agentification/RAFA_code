

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b f)
(ontable c)
(on d c)
(on e a)
(on f e)
(on g i)
(ontable h)
(on i d)
(clear b)
(clear g)
(clear h)
)
(:goal
(and
(on b c)
(on d i)
(on e a)
(on g f)
(on i e))
)
)


